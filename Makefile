run:
	docker-compose up --build -d

entrypoint:
	uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000

stop:
	docker-compose down

clean:
	docker-compose down --volumes
