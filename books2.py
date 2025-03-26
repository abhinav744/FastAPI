from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID

from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, book_to_return):
        self.book_to_return = book_to_return

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1,
                        max_length=100)
    description: Optional[str] = Field(title = "Description of the book",
                                       max_length=100,
                                       min_length=1)
    rating: int = Field(gt=-1,
                        lt=101)

    class Config:
        schema_extra = {
            "example" : {
                "id":"1a73dc70-353e-4e64-94f3-a991327954aa",
                "title": "computer pro",
                "author": "codewithroby",
                "description": "a nice description",
                "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str= Field(min_length=1)
    author: str
    description: Optional[str] = Field(None,
                                       title="description of book",
                                       max_length=100,
                                       min_length=1)

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418,
                        content={"message": f'hey why do you want {exception.book_to_return}'
                                 f'you need to study more'}
                        )

@app.post("/book/login")
async def book_login(book_id:int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "fastapiuser" and password == "test1234":
        return BOOKS[book_id]
    return "invalid user"

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header" : random_header}

@app.get("/")
async def read_all_books(book_to_return: Optional[int] = None):
    if book_to_return and book_to_return < 0:
        raise NegativeNumberException(book_to_return = book_to_return)

    if len(BOOKS) < 1:
        create_book_no_api()

    if book_to_return and len(BOOKS) >= book_to_return > 0:
        i = 1
        new_books = []
        while i <= book_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books

    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.get("/book/rating/{book_id}", response_model = BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
    raise raise_item_cannot_be_found_exception()

def create_book_no_api():
    book_1 = Book(id="5a73dc70-353e-4e64-94f3-a991327954aa",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="2a73dc70-353e-4e64-94f3-a991327954aa",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="3a73dc70-353e-4e64-94f3-a991327954aa",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="4a73dc70-353e-4e64-94f3-a991327954aa",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="book not found",
                         headers={"X-Header_Error":
                                  "nothing to be seen at UUID"})

