from flask import Flask, jsonify, request

app = Flask(__name__)


class Book:
    def __init__(self, id, title, author, year):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }


books = []
next_id = 1


def find_book(book_id):
    for book in books:
        if book_id == book.id:
            return book

    return None


def validate_book_data(data):
    errors = []

    if "title" not in data or not data["title"]:
        errors.append("title is required")
    if "author" not in data or not data["author"]:
        errors.append("author is required")
    if "year" not in data:
        errors.append("year is required")
    elif not isinstance(data["year"], int):
        errors.append("year must be a number")
    elif data["year"] < 1000:
        errors.append("please put a valid year")

    return errors


@app.route("/books")
def get_books():
    return jsonify([book.to_dict() for book in books])


@app.route("/books", methods=["POST"])
def add_book():
    global next_id

    data = request.get_json()

    errors = validate_book_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_book = Book(next_id, data["title"], data["author"], data["year"])
    books.append(new_book)
    next_id += 1

    return jsonify([book.to_dict() for book in books]), 201


@app.route("/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    global books
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Book Not Found"}), 404

    books = [book for book in books if book.id != book_id]

    result_books = [book.to_dict() for book in books]

    return jsonify(result_books), 200


@app.route("/books/<int:book_id>", methods=["PATCH"])
def edit_books(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Book Not Found"}), 404

    data = request.get_json()

    if "title" in data:
        if not data["title"]:
            return jsonify({"error": "Title not found"}), 400
        book.title = data["title"]

    if "author" in data:
        if not data["author"]:
            return jsonify({"error": "Author not found"}), 400
        book.author = data["author"]

    if "year" in data:
        if not data["year"]:
            return jsonify({"error": "Year not found"}), 400
        book.year = data["year"]

    return jsonify(book.to_dict()), 200


if __name__ == "__main__":
    app.run(debug=True)
