from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Member(Base):
    __tablename__ = 'members'
    member_id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Integer)
    email = Column(String, unique=True, index=True)
    address = Column(String)


class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    author = Column(String)
    genre = Column(String)
    total_stock = Column(Integer)
    available_stock = Column(Integer)


class BorrowRecord(Base):
    __tablename__ = 'borrow_records'
    borrow_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.member_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    borrow_date = Column(DateTime)
    due_date = Column(DateTime)
    return_date = Column(DateTime)

    member = relationship("Member")
    book = relationship("Book")
