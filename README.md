API is set up for use with Docker.

Build: ` docker-compose up -d --build`

Run tests: `docker-compose exec web pytest --cov --cov-report=html`