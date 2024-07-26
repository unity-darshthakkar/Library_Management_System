from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import engine, Base
from dependencies import get_db
from datetime import datetime
from typing import Optional
from models import User, Member, Book, BorrowRecord
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
app = FastAPI()


class user_Create(BaseModel):
    user_id: int
    name: str
    username: str
    password: str


class user_update(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class member_Create(BaseModel):
    member_id: int
    phone_number: int
    email: str
    address: str


class member_update(BaseModel):
    phone_number: Optional[int] = None
    email: Optional[str] = None
    address: Optional[str] = None


class book_Create(BaseModel):
    book_id: int
    name: str
    author: str
    genre: str
    total_stock: int
    available_stock: int


class book_update(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    total_stock: Optional[int] = None
    available_stock: Optional[int] = None


class borrow_Create(BaseModel):
    borrow_id: int
    member_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime


class borrow_update(BaseModel):
    member_id: Optional[int] = None
    book_id: Optional[int] = None
    borrow_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None


# User endpoints
@app.post("/users")
def create_user(request_body: user_Create, db: Session = Depends(get_db)):
    try:
        db_user = User(user_id=request_body.user_id, name=request_body.name, username=request_body.username,
                       password=request_body.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"data": db_user, "message": "User added successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")


@app.get("/users")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.put("/users/{user_id}")
def update_user(user_id: int, request_body: user_update, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Member not found")
        if request_body.name is not None:
            db_user.name = request_body.name
        if request_body.username is not None:
            db_user.username = request_body.username
        if request_body.password is not None:
            db_user.password = request_body.password
        db.commit()
        db.refresh(db_user)
        return {"data": db_user, "message": "User updated successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


# Member endpoints
@app.post("/members")
def create_member(request_body: member_Create, db: Session = Depends(get_db)):
    try:
        db_member = Member(member_id=request_body.member_id, phone_number=request_body.phone_number,
                           email=request_body.email, address=request_body.address)
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return {"data": db_member, "message": "Member added successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@app.get("/members")
def read_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    members = db.query(Member).offset(skip).limit(limit).all()
    return members


@app.put("/members/{member_id}")
def update_member(member_id: int, request_body: member_update, db: Session = Depends(get_db)):
    try:
        db_member = db.query(Member).filter(Member.member_id == member_id).first()
        if not db_member:
            raise HTTPException(status_code=404, detail="Member not found")
        if request_body.phone_number is not None:
            db_member.phone_number = request_body.phone_number
        if request_body.email is not None:
            db_member.email = request_body.email
        if request_body.address is not None:
            db_member.address = request_body.address
        db.commit()
        db.refresh(db_member)
        return {"data": db_member, "message": "Member updated successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.member_id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(db_member)
    db.commit()
    return {"detail": "Member deleted successfully"}


# Book endpoints
@app.post("/books")
def create_book(request_body: book_Create, db: Session = Depends(get_db)):
    try:
        db_book = Book(book_id=request_body.book_id, name=request_body.name, author=request_body.author,
                       genre=request_body.genre, total_stock=request_body.total_stock,
                       available_stock=request_body.available_stock)
        if request_body.available_stock > request_body.total_stock:
            raise HTTPException(status_code=400, detail="Available stock should be less or equal to than total stock")
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return {"data": db_book, "message": "Book added successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book name already exists")


@app.get("/books")
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books


@app.put("/books/{book_id}")
def update_book(book_id: int, request_body: book_update, db: Session = Depends(get_db)):
    try:
        db_book = db.query(Book).filter(Book.book_id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Member not found")
        if request_body.name is not None:
            db_book.name = request_body.name
        if request_body.author is not None:
            db_book.author = request_body.author
        if request_body.genre is not None:
            db_book.genre = request_body.genre
        if request_body.total_stock is not None:
            db_book.total_stock = request_body.total_stock
        if request_body.available_stock is not None:
            db_book.available_stock = request_body.available_stock
        if request_body.available_stock > request_body.total_stock:
            raise HTTPException(status_code=400, detail="Available stock should be less or equal to than total stock")
        db.commit()
        db.refresh(db_book)
        return {"data": db_book, "message": "Book updated successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}


# Borrow Endpoints
@app.post("/borrows")
def create_borrow_record(request_body: borrow_Create, db: Session = Depends(get_db)):
    try:
        db_member = db.query(Member).filter(Member.member_id == request_body.member_id).first()
        if not db_member:
            raise HTTPException(status_code=400, detail="Invalid member id")
        db_book = db.query(Book).filter(Book.book_id == request_body.book_id).first()
        if not db_book:
            raise HTTPException(status_code=400, detail="Invalid book id")
        db_borrow_record = BorrowRecord(borrow_id=request_body.borrow_id, member_id=request_body.member_id,
                                        book_id=request_body.book_id, borrow_date=request_body.borrow_date,
                                        due_date=request_body.due_date, return_date=request_body.return_date)
        if not request_body.due_date > request_body.borrow_date:
            raise HTTPException(status_code=400, detail="Due date should be later that borrow date")
        if not (request_body.borrow_date < request_body.return_date < request_body.due_date):
            raise HTTPException(status_code=400, detail="Return date is out of bounds")
        db.add(db_borrow_record)
        db.commit()
        db.refresh(db_borrow_record)
        return {"data": db_borrow_record, "message": "Borrow created successfully",
                "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Borrow record already exists for this member and book")


@app.get("/borrows")
def read_borrow_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    borrow_records = db.query(BorrowRecord).offset(skip).limit(limit).all()
    return borrow_records


@app.put("/borrows/{borrow_id}")
def update_borrow(borrow_id: int, request_body: borrow_update, db: Session = Depends(get_db)):
    try:
        db_borrow = db.query(BorrowRecord).filter(BorrowRecord.borrow_id == borrow_id).first()
        if not db_borrow:
            raise HTTPException(status_code=404, detail="Member not found")
        if request_body.member_id is not None:
            db_borrow.member_id = request_body.member_id
        if request_body.book_id is not None:
            db_borrow.book_id = request_body.book_id
        if request_body.borrow_date is not None:
            db_borrow.borrow_date = request_body.borrow_date
        if request_body.due_date is not None:
            db_borrow.due_date = request_body.due_date
        if request_body.return_date is not None:
            db_borrow.return_date = request_body.return_date
        if not request_body.due_date > request_body.borrow_date:
            raise HTTPException(status_code=400, detail="Due date should be later that borrow date")
        if not (request_body.borrow_date < request_body.return_date < request_body.due_date):
            raise HTTPException(status_code=400, detail="Return date is out of bounds")
        db.commit()
        db.refresh(db_borrow)
        return {"data": db_borrow, "message": "Borrow updated successfully", "status_code": status.HTTP_201_CREATED}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@app.delete("/borrows/{borrow_id}")
def delete_borrow_record(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow_record = db.query(BorrowRecord).filter(BorrowRecord.borrow_id == borrow_id).first()
    if not db_borrow_record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    db.delete(db_borrow_record)
    db.commit()
    return {"detail": "Borrow record deleted successfully"}
