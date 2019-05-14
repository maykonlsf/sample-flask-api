from flask import Flask
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from models.database import db

ma = Marshmallow()


class BookModel(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages


class BookSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    pages = fields.Integer(required=True)
