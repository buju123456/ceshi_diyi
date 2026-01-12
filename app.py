from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "books.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(50), nullable=True)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "available": self.available,
        }

@app.before_first_request
def create_tables():
    db.create_all()

# Frontend
@app.route("/")
def index():
    return render_template("index.html")

# API: 列表（可通过 ?search=keyword 搜索 title 或 author）
@app.route("/api/books", methods=["GET"])
def list_books():
    search = request.args.get("search", type=str)
    if search:
        q = "%{}%".format(search)
        books = Book.query.filter(
            db.or_(Book.title.ilike(q), Book.author.ilike(q))
        ).order_by(asc(Book.id)).all()
    else:
        books = Book.query.order_by(asc(Book.id)).all()
    return jsonify([b.to_dict() for b in books]), 200

# API: 获取单本
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    b = Book.query.get_or_404(book_id)
    return jsonify(b.to_dict()), 200

# API: 添加
@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json() or {}
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400
    year = data.get("year")
    isbn = data.get("isbn")
    available = data.get("available", True)
    book = Book(title=title, author=author, year=year, isbn=isbn, available=available)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

# API: 更新
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    b = Book.query.get_or_404(book_id)
    data = request.get_json() or {}
    b.title = data.get("title", b.title)
    b.author = data.get("author", b.author)
    b.year = data.get("year", b.year)
    b.isbn = data.get("isbn", b.isbn)
    if "available" in data:
        b.available = bool(data.get("available"))
    db.session.commit()
    return jsonify(b.to_dict()), 200

# API: 删除
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    b = Book.query.get_or_404(book_id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({"result": "deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
