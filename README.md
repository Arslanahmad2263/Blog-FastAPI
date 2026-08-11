# Blog API (FastAPI)

A simple, modular Blog API built with FastAPI. This repo provides user authentication (JWT), CRUD for posts, commenting, and ready-to-use development and deployment guidance.

> NOTE: This README is a full template — adjust environment variables, commands, and file paths to match your repository if anything differs.

## Features

- User registration and JWT-based authentication
- Create, read, update, delete (CRUD) blog posts
- Commenting on posts
- Pagination and basic filtering for list endpoints
- Automatic API docs (Swagger UI and ReDoc)
- Alembic migrations and SQLAlchemy/SQLModel examples

## Tech stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy or SQLModel
- Alembic (DB migrations)
- Pydantic (validation)
- PostgreSQL (recommended) or SQLite (dev)

## Quick start (development)

1. Clone the repo
   ```bash
   git clone https://github.com/Arslanahmad2263/Blog-FastAPI.git
   cd Blog-FastAPI
   ```

2. Create & activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS / Linux
   .\.venv\Scripts\activate       # Windows (PowerShell)
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (see example below) and export variables.

5. Run database migrations (if using Alembic)
   ```bash
   alembic upgrade head
   ```

6. Start the development server
   ```bash
   uvicorn app.main:app --reload
   ```

7. API docs
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Example .env

Create `.env` at project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/blogdb
SECRET_KEY=your-very-secret-jwt-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```
## API overview (example endpoints)

Authentication
- POST /auth/register — register a new user
- POST /auth/login — get JWT access token

Users
- GET /users/me — get current user profile

Posts
- GET /posts — list posts (pagination & filtering)
- POST /posts — create a post (auth required)
- GET /posts/{post_id} — get a post by id
- PUT /posts/{post_id} — update a post (auth + ownership)
- DELETE /posts/{post_id} — delete a post (auth + ownership)

Comments
- GET /posts/{post_id}/comments — list comments for a post
- POST /posts/{post_id}/comments — add a comment (auth required)

All endpoints available and testable in /docs.

## Authentication

This project uses JWT for stateless authentication.

Flow:
1. User logs in via /auth/login with email & password.
2. Server returns an access token (JWT).
3. Client sends token in header: Authorization: Bearer <token>.

Security tips:
- Use a strong SECRET_KEY and rotate it periodically.
- Use short-lived access tokens and consider refresh tokens for long sessions.
- Store tokens securely on the client (httpOnly cookies or secure storage).

## Database & migrations

- Configure Alembic to read DATABASE_URL from env for migrations.
- For local development you can use SQLite (sqlite:///./dev.db), but prefer PostgreSQL in production.

Migrate example:
```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

## Testing

- Tests use pytest.
- Use a separate test database or an in-memory SQLite DB for fast tests.
- Example:
```bash
pytest -q
```
Add fixtures in app/tests/conftest.py to provide a test client and test DB sessions.

## Linting & formatting

- black: `black .`
- isort: `isort .`
- flake8: `flake8`

## Contributing

Contributions are welcome:
1. Fork the repo.
2. Create a branch: `git checkout -b feat/your-feature`
3. Run tests & linters.
4. Open a pull request with a clear description.

## Author

Arslan Ahmad
