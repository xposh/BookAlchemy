import os
from flask import Flask, render_template, request # 'render_template' und 'request' später hinzugefügt
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# 1. Instanz
app = Flask(__name__)

#2
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template('home.html', books=all_books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        new_author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)

        # 'db.session' ist die aktive Verbindung zur library.sqlite
        db.session.add(new_author)
        db.session.commit()  # Erst hier werden die Daten physisch gespeichert

        return "Author successfully added!"

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Daten für das Buch aus dem Formular ziehen
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        year = request.form.get('publication_year')
        author_id = request.form.get('author_id')  # Das ist die ID vom ausgewählten Autor

        # Neues Buch-Objekt erstellen
        new_book = Book(isbn=isbn, title=title, publication_year=year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        return "Book successfully added!"

    # alle Autoren für Dropdown-Menü im Formular
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


#with app.app_context():
    #db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

