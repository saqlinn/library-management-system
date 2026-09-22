# Library Management System – Final Assessment

## Requirements covered

- SQLAlchemy ORM + MySQL
- FastAPI and Swagger at `/docs`
- Authentication: `/register`, `/login`, `/profile`
- Password hashing with bcrypt
- JWT authentication
- Roles: Admin, Librarian, Member
- Admin-only book deletion
- Custom exceptions
- Login, issue, warning and error logging
- Unit/integration tests using FastAPI `TestClient`
- CRUD, issue/return and issued-books report

## Project structure

```text
Library management sys/
├── main.py
├── database.py
├── models.py
├── exceptions.py
├── test_main.py
├── library.log          # created when the API runs/logs events
└── README.md
```

## Installation

Activate the virtual environment and install:

```powershell
pip install fastapi uvicorn sqlalchemy pymysql bcrypt python-jose[cryptography] pytest httpx
```

## Database

Make sure MySQL is running and `database.py` points to the correct database.

The `users` table must contain:

```text
user_id     INT          PRIMARY KEY AUTO_INCREMENT
username    VARCHAR(50)  UNIQUE NOT NULL
password    VARCHAR(100) NOT NULL
role        VARCHAR(20)  NOT NULL
```

The application expects the `books`, `members`, and `issue_transactions` tables already created.

## Run the API

```powershell
python -m uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## Authentication demo

1. `POST /register` creates a normal Member account.
2. `POST /login` verifies the password and returns a JWT.
3. Click Swagger's **Authorize** button and enter the JWT.
4. `GET /profile` returns the authenticated user's profile.
5. Admin users can use `DELETE /books/{book_id}`.

For a real deployment, create Admin/Librarian accounts through an authorized administrative/seed process; do not let public registration choose `Admin`.

## Run tests

```powershell
pytest -v
```

The test suite uses an in-memory SQLite database so tests do not modify the real MySQL database.

## Logs

`library.log` records:

- successful and failed login attempts
- successful and failed book issue attempts
- book return events
- unauthorized admin attempts
- unexpected application/database errors

Never log passwords or JWT tokens.

## API catalogue

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health/home message |
| POST | `/register` | Register Member |
| POST | `/login` | Authenticate and receive JWT |
| GET | `/profile` | Authenticated user's profile |
| GET | `/books` | List books |
| GET | `/books/{book_id}` | Get one book |
| POST | `/books` | Add book |
| PUT | `/books/{book_id}` | Update book |
| DELETE | `/books/{book_id}` | Delete book; Admin only |
| GET | `/members` | List members |
| GET | `/members/{member_id}` | Get one member |
| POST | `/members` | Add member |
| PUT | `/members/{member_id}` | Update member |
| DELETE | `/members/{member_id}` | Delete member |
| POST | `/issue-book` | Issue a book |
| POST | `/return-book` | Return a book |
| GET | `/issued-books` | Issue/return report |

## Final demo sequence

1. Register a Member.
2. Login and obtain JWT.
3. Authorize in Swagger.
4. Open `/profile`.
5. Demonstrate book CRUD.
6. Demonstrate member CRUD.
7. Issue a book and show reduced stock.
8. Return the book and show increased stock.
9. Open `/issued-books` for the report.
10. Demonstrate Admin-only deletion.
11. Run `pytest -v`.
12. Open `library.log` and show login/issue/error logs.
