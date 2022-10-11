import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME2, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME2
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.test_question = {"question": "What is the nearest planet to th sun", "answer": "Mercury","difficulty": "3","category":"1"}
        self.test_question_1 = {"question": "What is the nearest planet to th sun", "answer": "Mercury", "difficulty": "3"}
        self.test_quiz = {'quiz_category': {'type': 'Sports', 'id': '6'},'previous_questions': [10]}
        self.test_quiz_1 = {'quiz_category': {'type': 'Sports', 'id': '6'}}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    """
    Test for get questions to play the quiz
    """
    def test_for_retrive_quiz_questions(self):
        client = self.client()
        res = client.post('/quizzes', json=self.test_quiz)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value['success'], True)

    def test_422_if_full_data_are_not_passed(self):
        client = self.client()
        res = client.post('/quizzes', json=self.test_quiz_1)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 422)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "unprocessable")
        
    def test_for_404_if_not_found_methode(self):
        client = self.client()
        res = client.post('/quizzes/wer', json=self.test_quiz)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "resource not found")


    """
    Test for get questions based on category
    """
    def test_for_retrieve_questions_with_categoty(self):
        client = self.client()
        res = client.get('/categories/3/questions')
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value['success'], True)
        self.assertEqual(value['total_questions'], 3)
        self.assertEqual(value['current_category'], 3)
        self.assertEqual(len(value['questions']), 3)

    def test_for_retrieve_questions_with_out_categoty(self):
        client = self.client()
        res = client.get('/categories/100000000/questions')
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value['success'], True)
        self.assertEqual(value['total_questions'], 0)
        self.assertEqual(value['current_category'], 100000000)
        self.assertEqual(len(value['questions']), 0)

    def test_for_404_if_not_found_methode(self):
        client = self.client()
        res = client.get('/categories/100000000/questions/wer')
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "resource not found")

    """
    Test for search questions
    """
    def test_for_retrive_question_search_with_results(self):
        client = self.client()
        res = client.post("/search", json={"searchTerm": "title"})
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value["success"], True)
        self.assertEqual(len(value["questions"]), 2)
        #assure if the app return data
        self.assertTrue(value["total_questions"])

    def test_for_retrive_question_search_without_results(self):
        client = self.client()
        res = client.post("/search", json={"searchTerm": "aaaaaaaaaaaaaaaaa"})
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value["success"], True)
        self.assertEqual(len(value["questions"]), 0)
        self.assertEqual(value["total_questions"], 0)

    def test_for_422_if_correct_varaible_name_is_not_provided(self):
        client = self.client()
        res = client.post("/search", json={"sech": "titel"})
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 422)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "unprocessable")
       
    def test_for_404_if_methode_not_found(self):
        client = self.client()
        res = client.post("/search/a", json={"searchTerm": "titel"})
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "resource not found")
    """
    Test for create questions
    """
    def test_for_create_new_question(self):
        client = self.client()
        res = client.post("/questions", json=self.test_question)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value["success"], True)
        #assure if the app return data
        self.assertTrue(len(value["questions"]))
        self.assertTrue(value["created"])

    def test_for_405_if_question_creation_not_allowed(self):
        client = self.client()
        res = client.post("/questions/45", json=self.test_question)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 405)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "method not allowed")

    def test_for_422_if_fullfilled_data_is_not_provided(self):
        client = self.client()
        res = client.post("/questions", json=self.test_question_1)
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 422)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "unprocessable")

    """
    Test for delete questions
    """

    def test_for_delete_question(self):
        client = self.client()
        res = client.delete("/questions/10")
        value = json.loads(res.data)
        status_code = res.status_code

        question = Question.query.filter(Question.id == 10).one_or_none()
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value["success"], True)
        self.assertEqual(question, None)
        self.assertEqual(value["deleted"], 10)
        #assure if the app return data
        self.assertTrue(len(value["questions"]))
        self.assertTrue(value["total_questions"])

    def test_for_422_if_question_does_not_found(self):
        client = self.client()
        res = client.delete("/questions/1000")
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 422)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "unprocessable")
   
    def test_for_404_if_methode_not_found(self):
        client = self.client()
        res = client.delete("/questions/a")
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "resource not found")

    """
    Test for get paginated questions
    """
    def test_for_retrieve_paginated_questions(self):
        client = self.client()
        res = client.get("/questions")
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(value["success"], True)
        #assure if the app return data
        self.assertTrue(len(value["questions"]))
        self.assertTrue(value["total_questions"])
        self.assertTrue(len(value['categories']))
 
    def test_for_404_requesting_beyond_valid_page(self):
        client = self.client()
        res = client.get("/questions?page=1000")
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value["success"], False)
        self.assertEqual(value["message"], "resource not found")

    """
    Test for get categories
    """
    def test_for_retrieve_categories(self):
        client = self.client()
        res = client.get('/categories')
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 200)
        self.assertEqual(len(value['categories']), 6)
        self.assertEqual(value['success'], True)

        #assure if the app return data
        self.assertTrue(len(value['categories']))

    def test_for_404_non_existing_category(self):
        client = self.client()
        res = client.get('/categories/9999')
        value = json.loads(res.data)
        status_code = res.status_code
        #compare if app return the correct data
        self.assertEqual(status_code, 404)
        self.assertEqual(value['success'], False)
        self.assertEqual(value['message'], 'resource not found')


 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()