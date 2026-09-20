from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    questions = relationship("Question", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name!r})>"

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="questions")

    def __repr__(self):
        return f"<Question(id={self.id}, title={self.title!r})>"
