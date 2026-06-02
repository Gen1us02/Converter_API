import pytest
from unittest.mock import AsyncMock, patch
from app.utils.hash import get_password_hash


# ----- Currency endpoints -----
@pytest.mark.asyncio
async def test_exchange(async_client, mock_convert, mock_auth_dependency):
    mock_convert.return_value = 123.45
    response = await async_client.get(
        "/currency/exchange", params={"from": "USD", "to": "EUR", "amount": 100}
    )
    assert response.status_code == 200
    assert response.json() == {"value": 123.45}
    mock_convert.assert_awaited_once_with(amount=100, from_cur="USD", to_cur="EUR")


@pytest.mark.asyncio
async def test_live_currency(async_client, mock_live_currency, mock_auth_dependency):
    mock_live_currency.return_value = {"BYNUSD": 2, "BYNEUR": 3}
    response = await async_client.get(
        "/currency/live-currency",
        params={"from_cur": "BYN", "currencies": ["USD", "EUR"]},
    )
    assert response.status_code == 200
    assert response.json() == {"BYNUSD": 2, "BYNEUR": 3}


@pytest.mark.asyncio
async def test_currency_list(
    async_client, mock_get_currency_list, mock_auth_dependency
):
    mock_get_currency_list.return_value = {"BYN": "BYN", "USD": "USD"}
    response = await async_client.get("/currency/currency-list")
    assert response.status_code == 200
    assert response.json() == {"BYN": "BYN", "USD": "USD"}


# ----- Users endpoints -----
@pytest.mark.asyncio
async def test_register_success(async_client, mock_user_repo):
    fake_user = AsyncMock()
    fake_user.id = 1
    fake_user.username = "alice"
    fake_user.password = get_password_hash("secret123")
    mock_user_repo.create_user.return_value = fake_user

    response = await async_client.post(
        "/users/register", json={"username": "alice", "password": "secret123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data
    assert "hashed_password" in data
    mock_user_repo.create_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_conflict(async_client, mock_user_repo):
    mock_user_repo.create_user.side_effect = ValueError("User already exists")
    response = await async_client.post(
        "/users/register", json={"username": "alice", "password": "secret123"}
    )
    assert response.status_code == 409
    assert "User already exists" in response.text
    mock_user_repo.create_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_success(async_client, mock_user_repo):
    from app.db.models import User

    hashed = get_password_hash("correct_password")
    fake_user = User(id=1, username="bob", password=hashed)
    mock_user_repo.get_user.return_value = fake_user

    with patch(
        "app.api.endpoints.user.generate_jwt_token", new_callable=AsyncMock
    ) as mock_jwt:
        mock_jwt.return_value = "fake_token"
        response = await async_client.post(
            "/users/login",
            data={"username": "bob", "password": "correct_password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake_token"
    assert data["token_type"] == "bearer"
    mock_user_repo.get_user.assert_awaited_once_with("bob")
    mock_jwt.assert_awaited_once_with({"sub": "bob"})


@pytest.mark.asyncio
async def test_login_invalid_username(async_client, mock_user_repo):
    mock_user_repo.get_user.return_value = None
    response = await async_client.post(
        "/users/login",
        data={"username": "unknown", "password": "any"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "Invalid username" in response.text


@pytest.mark.asyncio
async def test_login_wrong_password(async_client, mock_user_repo):
    hashed = get_password_hash("real_pass")
    fake_user = AsyncMock()
    fake_user.password = hashed
    mock_user_repo.get_user.return_value = fake_user
    response = await async_client.post(
        "/users/login",
        data={"username": "bob", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "Incorrect password" in response.text


@pytest.mark.asyncio
async def test_get_user_success(async_client, mock_user_repo):
    fake_user = AsyncMock()
    fake_user.id = 5
    fake_user.username = "charlie"
    fake_user.password = "hashed_stub"
    mock_user_repo.get_user.return_value = fake_user
    response = await async_client.get("/users/charlie")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "charlie"
    assert data["id"] == 5
    mock_user_repo.get_user.assert_awaited_once_with("charlie")


@pytest.mark.asyncio
async def test_get_user_not_found(async_client, mock_user_repo):
    mock_user_repo.get_user.return_value = None
    response = await async_client.get("/users/missing")
    assert response.status_code == 404
    assert "User not found" in response.text


@pytest.mark.asyncio
async def test_delete_user_success(async_client, mock_user_repo):
    mock_user_repo.delete_user.return_value = 42
    response = await async_client.delete("/users/delete/alice")
    assert response.status_code == 200
    assert response.json() == {"delete_user_id": 42}
    mock_user_repo.delete_user.assert_awaited_once_with("alice")


@pytest.mark.asyncio
async def test_delete_user_not_found(async_client, mock_user_repo):
    mock_user_repo.delete_user.return_value = None
    response = await async_client.delete("/users/delete/ghost")
    assert response.status_code == 404
    assert "User not found" in response.text


@pytest.mark.asyncio
async def test_delete_user_conflict(async_client, mock_user_repo):
    fake_user = AsyncMock()
    fake_user.id = 1
    fake_user.username = "alice"
    mock_user_repo.get_user.return_value = fake_user
    mock_user_repo.delete_user.side_effect = ValueError("Foreign key constraint")
    response = await async_client.delete("/users/delete/alice")
    assert response.status_code == 404
    assert "User already exists" in response.text


@pytest.mark.asyncio
async def test_update_user_success(async_client, mock_user_repo):
    mock_user_repo.update_user.return_value = 7
    response = await async_client.put(
        "/users/update/alice",
        json={"username": "alice_new", "password": "newpassword123"},
    )
    assert response.status_code == 200
    assert response.json() == {"update_user_id": 7}
    args, _ = mock_user_repo.update_user.call_args
    assert args[0] == "alice"
    assert args[1].username == "alice_new"
    assert args[1].password == "newpassword123"


@pytest.mark.asyncio
async def test_update_user_not_found(async_client, mock_user_repo):
    mock_user_repo.update_user.return_value = None
    response = await async_client.put("/users/update/ghost", json={"username": "new"})
    assert response.status_code == 404
    assert "User not found" in response.text


@pytest.mark.asyncio
async def test_update_user_conflict(async_client, mock_user_repo):
    mock_user_repo.update_user.side_effect = ValueError("Username taken")
    response = await async_client.put(
        "/users/update/alice", json={"username": "occupied"}
    )
    assert response.status_code == 409
    assert "User already exists" in response.text


@pytest.mark.asyncio
async def test_update_user_invalid_password(async_client, mock_user_repo):
    response = await async_client.put("/users/update/alice", json={"password": "short"})
    assert response.status_code == 422
    mock_user_repo.update_user.assert_not_awaited()
