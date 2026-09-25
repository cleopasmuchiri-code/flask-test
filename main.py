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


if __name__ == "__main__":
    app.run(debug=True)
