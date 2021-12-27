from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "you_will_never_guess_this"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Book(db.Model):
    # __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    book_list = db.session.query(Book).all()
    return render_template("index.html", book_list=book_list)


@app.route("/create", methods=["GET", "POST"])
def create_book():

    if request.method == "POST":
        title = request.form.get("title")
        rating = request.form.get("rating")
        author = request.form.get("author")
        url = request.form.get("url")
        try:
            float(rating)
            new_book = Book(title=title, author=author, rating=rating, url=url)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("index"))
        except ValueError:
            flash("Rating has to be a valid number!")
            return render_template("create_book.html", title=title, author=author, url=url)
    return render_template("create_book.html")


@app.route("/reset")
def reset():
    flash("All inputs have been resetted!")
    return redirect(url_for("create_book"))


@app.route("/delete", methods=["GET", "POST"])
def delete():
    book_id = request.args.get("b_id")
    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD BY ID
        book_id = request.args.get("b_id")
        book_to_update = Book.query.get(book_id)
        new_rating = request.form["rating"]
        new_title = request.form["title"]
        new_url = request.form["url"]
        new_author = request.form["author"]
        try:
            float(new_rating)
            book_to_update.rating = new_rating
            book_to_update.author = new_author
            book_to_update.url = new_url
            book_to_update.title = new_title
            db.session.commit()
            return redirect(url_for("index"))
        except ValueError:
            flash("Rating has to be a valid number!")
            return render_template("edit.html", book=book_to_update)
    book_id = request.args.get("b_id")
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
