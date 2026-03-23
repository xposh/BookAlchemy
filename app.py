import os
from flask import Flask, render_template, request # 'render_template' und 'request' später hinzugefügt
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# 1. Instanz
app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/')
def home():
    search_query = request.args.get('search')
    sort_by = request.args.get('sort', 'title')

    query = Book.query

    if search_query:
        query = query.filter(Book.title.ilike(f'%{search_query}%'))


    if sort_by == 'author':
        query = query.join(Author).order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    all_books = query.all()

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
        db.session.commit()

        return "Author successfully added!"

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

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

from flask import Flask, render_template, request, redirect


@app.route('/delete_book/<id>')
def delete_book(id):
    # 1. Das Buch finden
    book = Book.query.get(id)
    author = book.author
    # 2. Buch löschen
    db.session.delete(book)
    db.session.commit()


    if len(author.books) == 0:
        db.session.add(author)
        db.session.delete(author)
        db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

