from sqlalchemy import Column, Integer, String, Date
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    
class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    isbn = Column(String)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    copies_available = Column(Integer)
    created_date = Column(Date)


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    member_type = Column(String)
    status = Column(String)

class IssueTransaction(Base):
    __tablename__ = "issue_transactions"

    transaction_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    member_id = Column(Integer)
    issue_date = Column(Date)
    return_date = Column(Date)