from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from main import app
from app.core.security import get_current_user
from app.repositories.user_repository import get_user_repository


# ----- Клиент для тестирования эндпоинтов -----
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# ----- Переопределение зависимости авторизации -----
@pytest_asyncio.fixture
def mock_auth_dependency():
    async def mock_get_current_user():
        return "test_user"

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


# ----- Переопределение репозитория (мок) -----
@pytest_asyncio.fixture
def mock_user_repo():
    mock_repo = AsyncMock()

    async def override_get_user_repository():
        return mock_repo

    app.dependency_overrides[get_user_repository] = override_get_user_repository
    yield mock_repo
    app.dependency_overrides.pop(get_user_repository, None)


# ----- Моки внешних API -----
@pytest_asyncio.fixture
def mock_convert():
    with patch("app.api.endpoints.currency.convert", new_callable=AsyncMock) as mock:
        yield mock


@pytest_asyncio.fixture
def mock_live_currency():
    with patch(
        "app.api.endpoints.currency.live_currency", new_callable=AsyncMock
    ) as mock:
        yield mock


@pytest_asyncio.fixture
def mock_get_currency_list():
    with patch(
        "app.api.endpoints.currency.get_currency_list", new_callable=AsyncMock
    ) as mock:
        yield mock
