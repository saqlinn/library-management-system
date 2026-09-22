import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from database import Base
from models import Book, Member, User


# In-memory SQLite database for tests.
# This keeps tests independent from your real MySQL database.
TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=TEST_ENGINE,
)

Base.metadata.create_all(bind=TEST_ENGINE)
main.SessionLocal = TestingSessionLocal

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


def create_member():
    db = TestingSessionLocal()
    member = Member(
        name="Test Member",
        email="test@example.com",
        member_type="Student",
        status="Active",
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    member_id = member.member_id
    db.close()
    return member_id


def create_book(copies=2):
    db = TestingSessionLocal()
    book = Book(
        isbn="ISBN-TEST",
        title="Test Book",
        author="Test Author",
        category="Testing",
        copies_available=copies,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    book_id = book.book_id
    db.close()
    return book_id


def create_user(username="member1", password="password123", role="Member"):
    db = TestingSessionLocal()
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")
    user = User(username=username, password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.user_id
    db.close()
    return user_id


# ---------------------------------------------------------
# Authentication unit/integration tests
# ---------------------------------------------------------
def test_register():
    response = client.post(
        "/register",
        json={"username": "newuser", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "Member"


def test_login():
    create_user()

    response = client.post(
        "/login",
        json={"username": "member1", "password": "password123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "Member"


def test_login_wrong_password():
    create_user()

    response = client.post(
        "/login",
        json={"username": "member1", "password": "wrongpass"},
    )

    assert response.status_code == 401


def test_profile_with_jwt():
    create_user()

    login_response = client.post(
        "/login",
        json={"username": "member1", "password": "password123"},
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/profile",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "member1"


# ---------------------------------------------------------
# Book tests
# ---------------------------------------------------------
def test_add_book():
    response = client.post(
        "/books",
        json={
            "isbn": "ISBN001",
            "title": "Python Basics",
            "author": "John",
            "category": "Programming",
            "copies_available": 5,
        },
    )

    assert response.status_code == 200
    assert "book_id" in response.json()


def test_get_books():
    create_book()

    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Book"


def test_get_book_not_found():
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_update_book():
    book_id = create_book()

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "Updated Book",
            "author": "New Author",
            "category": "Programming",
            "copies_available": 5,
        },
    )

    assert response.status_code == 200


def test_delete_book_admin_only():
    book_id = create_book()

    create_user(
        username="admin1",
        password="admin123",
        role="Admin",
    )

    login_response = client.post(
        "/login",
        json={"username": "admin1", "password": "admin123"},
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_member_cannot_delete_book():
    book_id = create_book()
    create_user()

    login_response = client.post(
        "/login",
        json={"username": "member1", "password": "password123"},
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------
# Member tests
# ---------------------------------------------------------
def test_add_member():
    response = client.post(
        "/members",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "member_type": "Student",
            "status": "Active",
        },
    )

    assert response.status_code == 200
    assert "member_id" in response.json()


def test_get_member_not_found():
    response = client.get("/members/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


def test_update_member():
    member_id = create_member()

    response = client.put(
        f"/members/{member_id}",
        json={
            "name": "Updated Member",
            "email": "updated@example.com",
            "member_type": "Faculty",
            "status": "Active",
        },
    )

    assert response.status_code == 200


def test_delete_member():
    member_id = create_member()

    response = client.delete(f"/members/{member_id}")

    assert response.status_code == 200


# ---------------------------------------------------------
# Transaction tests
# ---------------------------------------------------------
def test_issue_book():
    book_id = create_book(copies=2)
    member_id = create_member()

    response = client.post(
        "/issue-book",
        json={
            "book_id": book_id,
            "member_id": member_id,
        },
    )

    assert response.status_code == 200
    assert "transaction_id" in response.json()


def test_issue_unavailable_book():
    book_id = create_book(copies=0)
    member_id = create_member()

    response = client.post(
        "/issue-book",
        json={
            "book_id": book_id,
            "member_id": member_id,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No copies available"


def test_issue_missing_member():
    book_id = create_book(copies=2)

    response = client.post(
        "/issue-book",
        json={
            "book_id": book_id,
            "member_id": 999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


def test_return_book():
    book_id = create_book(copies=2)
    member_id = create_member()

    issue_response = client.post(
        "/issue-book",
        json={
            "book_id": book_id,
            "member_id": member_id,
        },
    )

    assert issue_response.status_code == 200

    response = client.post(
        "/return-book",
        json={
            "book_id": book_id,
            "member_id": member_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Book returned successfully"


def test_issued_books_report():
    book_id = create_book(copies=2)
    member_id = create_member()

    client.post(
        "/issue-book",
        json={
            "book_id": book_id,
            "member_id": member_id,
        },
    )

    response = client.get("/issued-books")

    assert response.status_code == 200
    assert len(response.json()) == 1
