import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, fetch_questions):

    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in fetch_questions]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    Set up CORS. Allow '*' for origins
    """
    CORS(app, resources={'/': {'origins': '*'}})
    """
    after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    An endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        question_type = Category.query.order_by(Category.id)
        question_types = question_type.all()
        num_question_type = question_type.count()
        if  not num_question_type == 0:
            fetch_question_type = {}
            index = 0
            while index < num_question_type:
                fetch_question_type.update({question_types[index].id: 
                                            question_types[index].type})
                index += 1
            return jsonify({"success": True, "categories": fetch_question_type})
        else:
             abort(404)
    """
    An endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the 
    bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        fetch_question = Question.query.order_by(Question.id)
        fetch_questions = fetch_question.all()
        num_selections = fetch_question.count()
        if not num_selections == 0:
            question_type = Category.query.order_by(Category.id)
            question_types = question_type.all()
            num_question_type = question_type.count()
            fetch_question_type = {}
            index = 0
            while index < num_question_type:
                fetch_question_type.update({question_types[index].id: 
                                            question_types[index].type})
                index += 1
            if len(paginate_questions(request, fetch_questions)) == 0:
                abort(404)
            total_questions = len(Question.query.all())
            return jsonify({
                "success": True, 
                "questions": paginate_questions(request, fetch_questions), 
                "total_questions": total_questions,
                "categories": fetch_question_type
            })
        else:
            abort(404)

    """
    An endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, 
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            fetch_delete_questions = Question.query.filter(Question.id == question_id).one_or_none()
            if not fetch_delete_questions is None:
                fetch_delete_questions.delete()
                fetch_question = Question.query.order_by(Question.id)
                fetch_questions = fetch_question.all()
                num_fetch_questions =fetch_question.count()
                return jsonify({
                    "success": True,
                    "deleted": question_id,
                    "questions": paginate_questions(request, fetch_questions), 
                    "total_questions":num_fetch_questions
                })
            else:
                abort(404)
        except:
            abort(422)
        
    """
    An endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear 
    at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        if request.get_json().get('question', None) and request.get_json().get('answer', 
        None) and request.get_json().get('difficulty', 
        None) and request.get_json().get('category', None): 
            add_new_question = Question(question=request.get_json().get('question', None),
            answer=request.get_json().get('answer', None),
            difficulty=request.get_json().get('difficulty', None),
            category=request.get_json().get('category', None))
            if add_new_question is None:
                abort(404)
            add_new_question.insert()
            fetch_question = Question.query.order_by(Question.id)
            fetch_questions = fetch_question.all()
            num_fetch_questions = fetch_question.count()
            return jsonify({
                "success": True,
                "created": add_new_question.id,
                "questions": paginate_questions(request, fetch_questions),
                "total_questions": num_fetch_questions
            })
        else:
            abort(422)
    """
    An endpoint to get questions based on a search term.
    which will return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json().get('searchTerm', None)
        if search_term is None:
            abort(422)
        find_word = Question.question.ilike(f'%{search_term}%')
        fetch_questions = Question.query.filter(find_word).all()
        if fetch_questions is None:
            abort(404)
        num_fetch_questions = len(fetch_questions)
        return jsonify({
            "success": True,
            "questions": paginate_questions(request, fetch_questions),
            "total_questions":num_fetch_questions,
            "current_category": None
        })

    """
    An endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        if category_id is None:
            abort(422)
        fetch_questions = Question.query.filter(
            Question.category == str(category_id)).all()
        if fetch_questions is None:
            abort(404)
        num_fetch_questions = len(fetch_questions)
        return jsonify({
            "success": True,
            "current_category": category_id,
            "questions": paginate_questions(request, fetch_questions),
            "total_questions": num_fetch_questions
        })

    """
    An endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def retrive_quiz_questions():
        question_type = request.get_json().get('quiz_category')
        last_quiz = request.get_json().get('previous_questions')
        if question_type and last_quiz is None:
            abort(422)
        question_type_id = question_type['id']
        fetch_different_questions = Question.id.notin_((last_quiz))
        if question_type_id == 0:
            fetch_question = Question.query.filter(fetch_different_questions)
            fetch_all_questions = fetch_question.all()
        else:
            fetch_question = Question.query.filter_by(
                category = question_type_id).filter(fetch_different_questions)
            fetch_all_questions = fetch_question.all()
        len_questions = len(fetch_all_questions)
        if len_questions <= 0:
            return jsonify({"success": True, "question": None})
        else:
            random_questions = fetch_all_questions[
                random.randrange(0, len_questions)]
            format_questions = random_questions.format()
            return jsonify({
                "success": True, 
                "question": format_questions
            })

    """
    ERROR HANDLERS 
    """
    """
    error handlers for 404.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"}),
            404,
        )
    """
    error handlers for 422.
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"}),
            422,
        )
    """
    error handlers for 405.
    """
    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"}),
            405,
        )
    return app