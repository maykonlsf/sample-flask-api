from http import HTTPStatus
from flask_restful import Resource, abort, request

from models.database import db
from models.books import BookModel, BookSchema

books_schema = BookSchema(many=True)
book_schema = BookSchema()

class Book(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {"error": "bad request"}, HTTPStatus.BAD_REQUEST
        
        data, errors = book_schema.load(json_data)
        if errors:
            return errors, HTTPStatus.BAD_REQUEST

        book = BookModel(data["title"], data["pages"])

        db.session.add(book)
        db.session.commit()

        result = book_schema.dump(book).data
        return result, HTTPStatus.CREATED

    def put(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {"error": "bad request"}, HTTPStatus.BAD_REQUEST
        
        data, errors = book_schema.load(json_data)
        if errors:
            return errors, HTTPStatus.BAD_REQUEST
        
        book = BookModel.query.filter_by(id=id).first()
        if not book:
            return {"error": f"book '{id}' not found"}, HTTPStatus.NOT_FOUND
        book.title = json_data["title"]
        book.pages = json_data["pages"]
        db.session.commit()

        return book_schema.dump(book).data, HTTPStatus.NO_CONTENT

    def get(self, id=None):
        if id is None:
            books = BookModel.query.all()
            books = books_schema.dump(books).data
            return books
        else:
            book = BookModel.query.filter_by(id=id).first()
            if book:
                return book_schema.dump(book).data
            else:
                return {"error": f"book '{id}' not found"}, HTTPStatus.NOT_FOUND

    def delete(self, id):
        book = BookModel.query.filter_by(id=id).delete()
        db.session.commit()
        if book:
            return book_schema.dump(book).data, 204
        else:
            return {"error": f"book '{id}' not found"}, HTTPStatus.NOT_FOUND
