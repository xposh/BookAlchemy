from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    # Tabellenname (optional, aber Best Practice)
    __tablename__ = 'authors'

    # Spalten-Definitionen
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __str__(self):
        return f"Author(id={self.id}, name='{self.name}')"


    class Book(db.Model):
        __tablename__ = 'books'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        isbn = db.Column(db.String, unique=True)
        title = db.Column(db.String, nullable=False)
        publication_year = db.Column(db.Integer)

        # Der Foreign Key (Fremdschlüssel)
        author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

        def __str__(self):
            return f"Book(id={self.id}, title='{self.title}')"