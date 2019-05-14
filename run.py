from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from resources.book_resource import Book


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    CORS(app)
    api = Api(app)
    api.add_resource(Book, '/books', '/books/<int:id>')

    from models.database import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)