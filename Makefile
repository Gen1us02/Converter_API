run:
	docker run -d -p 8000:8000 --env-file ./.env --rm --name converter-api-cont converter-api

stop:
	docker stop converter-api-cont