from datetime import date, datetime, timedelta, timezone
import logging

import bcrypt
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import BaseModel, Field

from database import SessionLocal
from models import Book, Member, IssueTransaction, User
from exceptions import (
    BookNotFoundException,
    MemberNotFoundException,
    BookUnavailableException,
)

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# JWT settings
# ---------------------------------------------------------
SECRET_KEY = "my-library-secret-key"  # Use an environment variable in production.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def create_access_token(username: str, role: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "username": username,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except Exception:
        logger.warning("Invalid or expired JWT token")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


def require_admin(user_data: dict = Depends(get_current_user)):
    if user_data.get("role") != "Admin":
        logger.warning(
            f"Unauthorized admin action by user: {user_data.get('username')}"
        )
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return user_data


# ---------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------
app = FastAPI(
    title="Library Management API",
    description="Library Management System using FastAPI and SQLAlchemy ORM",
    version="1.0.0",
)


# ---------------------------------------------------------
# Custom exception handlers
# ---------------------------------------------------------
@app.exception_handler(BookNotFoundException)
async def book_not_found_handler(
    request: Request,
    exc: BookNotFoundException,
):
    logger.warning(str(exc))
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(MemberNotFoundException)
async def member_not_found_handler(
    request: Request,
    exc: MemberNotFoundException,
):
    logger.warning(str(exc))
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(BookUnavailableException)
async def book_unavailable_handler(
    request: Request,
    exc: BookUnavailableException,
):
    logger.warning(str(exc))
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


# ---------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------
class BookCreate(BaseModel):
    isbn: str = Field(min_length=1)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    category: str = Field(min_length=1)
    copies_available: int = Field(ge=0)


class BookUpdate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    category: str = Field(min_length=1)
    copies_available: int = Field(ge=0)


class MemberCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    member_type: str = Field(min_length=1)
    status: str = Field(min_length=1)


class MemberUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    member_type: str = Field(min_length=1)
    status: str = Field(min_length=1)


class IssueBookRequest(BaseModel):
    book_id: int
    member_id: int


class ReturnBookRequest(BaseModel):
    book_id: int
    member_id: int


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=50)


class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Library Management API is running"}


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------
@app.post("/register")
def register(user: RegisterRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.username == user.username
        ).first()

        if existing_user is not None:
            return {"message": "Username already exists"}

        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"),
            bcrypt.gensalt(),
        )

        new_user = User(
            username=user.username,
            password=hashed_password.decode("utf-8"),
            role="Member",
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"New user registered: {new_user.username}")

        return {
            "message": "User registered successfully",
            "user_id": new_user.user_id,
            "username": new_user.username,
            "role": new_user.role,
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Registration error for {user.username}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Registration failed",
        )
    finally:
        db.close()


@app.post("/login")
def login(user: LoginRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.username == user.username
        ).first()

        if existing_user is None:
            logger.warning(
                f"Failed login attempt for username: {user.username}"
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        password_match = bcrypt.checkpw(
            user.password.encode("utf-8"),
            existing_user.password.encode("utf-8"),
        )

        if not password_match:
            logger.warning(
                f"Failed login attempt for username: {user.username}"
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        logger.info(
            f"User {existing_user.username} logged in successfully"
        )

        access_token = create_access_token(
            existing_user.username,
            existing_user.role,
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": existing_user.user_id,
            "username": existing_user.username,
            "role": existing_user.role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {user.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")
    finally:
        db.close()


@app.get("/profile")
def get_profile(user_data: dict = Depends(get_current_user)):
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.username == user_data["username"]
        ).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
        }
    finally:
        db.close()


# ---------------------------------------------------------
# Books
# ---------------------------------------------------------
@app.get("/books")
def get_books():
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        return [
            {
                "book_id": book.book_id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "copies_available": book.copies_available,
                "created_date": book.created_date,
            }
            for book in books
        ]
    except Exception as e:
        logger.error(f"Get books error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to get books")
    finally:
        db.close()


@app.get("/books/{book_id}")
def get_book(book_id: int):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.book_id == book_id).first()

        if book is None:
            raise BookNotFoundException("Book not found")

        return {
            "book_id": book.book_id,
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "copies_available": book.copies_available,
            "created_date": book.created_date,
        }
    finally:
        db.close()


@app.post("/books")
def add_book(book: BookCreate):
    db = SessionLocal()
    try:
        new_book = Book(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            category=book.category,
            copies_available=book.copies_available,
            created_date=date.today(),
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "message": "Book added successfully",
            "book_id": new_book.book_id,
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Add book error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to add book")
    finally:
        db.close()


@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    db = SessionLocal()
    try:
        existing_book = db.query(Book).filter(
            Book.book_id == book_id
        ).first()

        if existing_book is None:
            raise BookNotFoundException("Book not found")

        existing_book.title = book.title
        existing_book.author = book.author
        existing_book.category = book.category
        existing_book.copies_available = book.copies_available

        db.commit()

        return {"message": "Book updated successfully"}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    user_data: dict = Depends(require_admin),
):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(
            Book.book_id == book_id
        ).first()

        if book is None:
            raise BookNotFoundException("Book not found")

        db.delete(book)
        db.commit()

        logger.info(
            f"Book {book_id} deleted by admin {user_data['username']}"
        )

        return {"message": "Book deleted successfully"}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ---------------------------------------------------------
# Members
# ---------------------------------------------------------
@app.get("/members")
def get_members():
    db = SessionLocal()
    try:
        members = db.query(Member).all()
        return [
            {
                "member_id": member.member_id,
                "name": member.name,
                "email": member.email,
                "member_type": member.member_type,
                "status": member.status,
            }
            for member in members
        ]
    except Exception as e:
        logger.error(f"Get members error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to get members")
    finally:
        db.close()


@app.get("/members/{member_id}")
def get_member(member_id: int):
    db = SessionLocal()
    try:
        member = db.query(Member).filter(
            Member.member_id == member_id
        ).first()

        if member is None:
            raise MemberNotFoundException("Member not found")

        return {
            "member_id": member.member_id,
            "name": member.name,
            "email": member.email,
            "member_type": member.member_type,
            "status": member.status,
        }
    finally:
        db.close()


@app.post("/members")
def add_member(member: MemberCreate):
    db = SessionLocal()
    try:
        new_member = Member(
            name=member.name,
            email=member.email,
            member_type=member.member_type,
            status=member.status,
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        return {
            "message": "Member added successfully",
            "member_id": new_member.member_id,
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Add member error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to add member")
    finally:
        db.close()


@app.put("/members/{member_id}")
def update_member(member_id: int, member: MemberUpdate):
    db = SessionLocal()
    try:
        existing_member = db.query(Member).filter(
            Member.member_id == member_id
        ).first()

        if existing_member is None:
            raise MemberNotFoundException("Member not found")

        existing_member.name = member.name
        existing_member.email = member.email
        existing_member.member_type = member.member_type
        existing_member.status = member.status

        db.commit()

        return {"message": "Member updated successfully"}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    db = SessionLocal()
    try:
        member = db.query(Member).filter(
            Member.member_id == member_id
        ).first()

        if member is None:
            raise MemberNotFoundException("Member not found")

        db.delete(member)
        db.commit()

        return {"message": "Member deleted successfully"}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ---------------------------------------------------------
# Transactions
# ---------------------------------------------------------
@app.post("/issue-book")
def issue_book(request: IssueBookRequest):
    db = SessionLocal()

    try:
        book = db.query(Book).filter(
            Book.book_id == request.book_id
        ).first()

        if book is None:
            raise BookNotFoundException("Book not found")

        if book.copies_available <= 0:
            raise BookUnavailableException("No copies available")

        member = db.query(Member).filter(
            Member.member_id == request.member_id
        ).first()

        if member is None:
            raise MemberNotFoundException("Member not found")

        transaction = IssueTransaction(
            book_id=request.book_id,
            member_id=request.member_id,
            issue_date=date.today(),
            return_date=None,
        )

        db.add(transaction)
        book.copies_available -= 1

        db.commit()
        db.refresh(transaction)

        logger.info(
            f"Book {request.book_id} issued to member {request.member_id}"
        )

        return {
            "message": "Book issued successfully",
            "transaction_id": transaction.transaction_id,
        }

    except (
        BookNotFoundException,
        MemberNotFoundException,
        BookUnavailableException,
    ):
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Error while issuing book {request.book_id} "
            f"to member {request.member_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while issuing the book",
        )
    finally:
        db.close()


@app.post("/return-book")
def return_book(request: ReturnBookRequest):
    db = SessionLocal()

    try:
        transaction = db.query(IssueTransaction).filter(
            IssueTransaction.book_id == request.book_id,
            IssueTransaction.member_id == request.member_id,
            IssueTransaction.return_date.is_(None),
        ).first()

        if transaction is None:
            logger.warning(
                f"Return failed - No active issue for book "
                f"{request.book_id} and member {request.member_id}"
            )
            raise HTTPException(
                status_code=404,
                detail="No active issue found",
            )

        transaction.return_date = date.today()

        book = db.query(Book).filter(
            Book.book_id == request.book_id
        ).first()

        if book is None:
            raise BookNotFoundException("Book not found")

        book.copies_available += 1

        db.commit()

        logger.info(
            f"Book {request.book_id} returned by member {request.member_id}"
        )

        return {"message": "Book returned successfully"}

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ---------------------------------------------------------
# Reports
# ---------------------------------------------------------
@app.get("/issued-books")
def get_issued_books():
    db = SessionLocal()

    try:
        results = (
            db.query(
                IssueTransaction.transaction_id,
                Book.book_id,
                Book.title,
                Member.member_id,
                Member.name.label("member_name"),
                IssueTransaction.issue_date,
                IssueTransaction.return_date,
            )
            .join(
                Book,
                IssueTransaction.book_id == Book.book_id,
            )
            .join(
                Member,
                IssueTransaction.member_id == Member.member_id,
            )
            .all()
        )

        return [
            {
                "transaction_id": transaction.transaction_id,
                "book_id": transaction.book_id,
                "title": transaction.title,
                "member_id": transaction.member_id,
                "member_name": transaction.member_name,
                "issue_date": transaction.issue_date,
                "return_date": transaction.return_date,
            }
            for transaction in results
        ]
    except Exception as e:
        logger.error(f"Get issued books error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Unable to get issued books report",
        )
    finally:
        db.close()
