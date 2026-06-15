from flask import Flask, make_response, request

app = Flask("library")

# Simulating a database table with rows
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
]


def get_book_from_db(book_id):
    return next((book for book in books if book["id"] == book_id), None)


@app.get("/books")
def get_books():
    return make_response(books)


@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = get_book_from_db(book_id)
    if book:
        return make_response(book, 200)
    return make_response({"message": "Book not found"}, 404)


@app.post("/books")
def create_book():
    new_book = request.get_json()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return make_response(new_book, 201)


@app.put("/books/<int:book_id>")
def update_book(book_id):
    book = get_book_from_db(book_id)
    if not book:
        return make_response({"message": "Book not found"}, 404)
    update_data = request.get_json()
    book.update(update_data)
    return make_response(book)


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return make_response({"message": "Book deleted"})


@app.get("/books/<int:book_id>/bookmarks")
def get_bookmarks(book_id):
    book = get_book_from_db(book_id)
    if not book:
        return make_response({"message": "Book not found"}, 404)
    return make_response(book.get("bookmarks", []))


@app.post("/books/<int:book_id>/bookmarks")
def add_bookmark(book_id):
    book = get_book_from_db(book_id)
    if not book:
        return make_response({"message": "Book not found"}, 404)
    new_bookmark = request.get_json()
    book.setdefault("bookmarks", []).append(new_bookmark)
    return make_response(new_bookmark, 201)




if __name__ == "__main__":
    app.run(debug=True)

