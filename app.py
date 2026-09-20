from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from models import db, Category, Question
from schemas.question import CategoryCreate, CategoryResponse, QuestionCreate, QuestionResponse

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///practicum3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

def validation_error(exc):
    return jsonify({"error": "Validation error", "details": exc.errors()}), 400

@app.get("/")
def index():
    return jsonify({
        "message": "Questions API — Homework 5 & 6",
        "endpoints": {
            "categories": ["GET /categories", "POST /categories", "PUT /categories/<id>", "DELETE /categories/<id>"],
            "questions": ["GET /questions", "POST /questions"]
        }
    })

@app.post("/categories")
def create_category():
    try:
        data = CategoryCreate.model_validate(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return validation_error(exc)
    category = Category(name=data.name.strip())
    if not category.name:
        return jsonify({"error": "Category name cannot be empty"}), 400
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category with this name already exists"}), 409
    return jsonify(CategoryResponse.model_validate(category).model_dump()), 201

@app.get("/categories")
def get_categories():
    categories = Category.query.order_by(Category.id).all()
    return jsonify([CategoryResponse.model_validate(c).model_dump() for c in categories])

@app.put("/categories/<int:category_id>")
def update_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404
    try:
        data = CategoryCreate.model_validate(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return validation_error(exc)
    category.name = data.name.strip()
    if not category.name:
        return jsonify({"error": "Category name cannot be empty"}), 400
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category with this name already exists"}), 409
    return jsonify(CategoryResponse.model_validate(category).model_dump())

@app.delete("/categories/<int:category_id>")
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404
    # Questions are retained and become uncategorized.
    for question in category.questions:
        question.category = None
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Category {category_id} deleted"})

@app.get("/questions")
def get_questions():
    questions = Question.query.order_by(Question.id).all()
    return jsonify([QuestionResponse.model_validate(q).model_dump() for q in questions])

@app.post("/questions")
def create_question():
    try:
        data = QuestionCreate.model_validate(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return validation_error(exc)
    category = None
    if data.category_id is not None:
        category = db.session.get(Category, data.category_id)
        if category is None:
            return jsonify({"error": "Category not found"}), 404
    question = Question(title=data.title.strip(), text=data.text.strip(), category=category)
    if not question.title or not question.text:
        return jsonify({"error": "Title and text cannot be empty"}), 400
    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionResponse.model_validate(question).model_dump()), 201

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
