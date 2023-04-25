# upgraded-journey

API is set up for use with Docker.\
Provides two versions:

- /v1: one endpoint for all data
- /v2: separate endpoints

Build: `docker-compose up -d --build`

Run tests: `docker-compose exec web pytest --cov --cov-report=html`

### Features:
* Async FastAPI endpoints
* Async SQLAlchemy connection using asyncpg for main DB connection and aiosqlite for testing. 
* OAuth2 + JWT authentication

### ERD

![ERD](docs/ERD_1.png)

### Deployment test

https://upgraded-journey-production.up.railway.app/ 

Example request: `https://upgraded-journey-production.up.railway.app/v2/passages/?skip=0&limit=100`