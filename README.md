# Trivia API

This Trivia API project is a game where users play it by answering different questions in different Categoty of questions. The task for this project was to create an API and which do the functionality:

-Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
-Delete questions.
-Add questions and require that they include question and answer text.
-Search for questions based on a text query string.
-Play the quiz game, randomizing either all questions or within a specific category.

In this project i learned how to implement well formatted API endpoints and enhance my knowledge on HTTP and API development best practices. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


## Getting Started

### Pre-requisites and Local Development 

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 405: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns all list of categories(types of questions).
- Sample: `curl http://127.0.0.1:5000/categories`

```   {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
```

### Endpoints 
#### GET /questions
- General:
    - Returns lists of questions,all lists of categories and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

```{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment"
        ,"6":"Sports"
        },
    "questions":[{
        "answer":"Tom Cruise",
        "category":"5",
        "difficulty":4,
        "id":4,
        "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {"answer":"Maya Angelou",
         "category":"4",
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
         },
         {"answer":"Edward Scissorhands",
         "category":"5",
         "difficulty":3,
         "id":6,
         "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
         {"answer":"Brazil",
         "category":"6",
         "difficulty":3,
         "id":10,
         "question":"Which is the only team to play in every soccer World Cup tournament?"
         },
         {"answer":"Uruguay",
          "category":"6",
          "difficulty":4,
          "id":11,
          "question":"Which country won the first ever soccer World Cup in 1930?"
          },
          {"answer":"George  Washington Carver",
          "category":"4",
          "difficulty":2,
          "id":12,
          "question":"Who invented Peanut Butter?"
          },
          {"answer":"Lake Victoria",
            "category":"3",
            "difficulty":2,
            "id":13,
            "question":"What is the largest lake in Africa?"
          },
          {"answer":"The Palace of Versailles",
           "category":"3",
           "difficulty":3,
           "id":14,
           "question":"In which royal palace would you find the Hall of Mirrors?"
           },
           {"answer":"Escher",
            "category":"2",
            "difficulty":1,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {"answer":"One",
            "category":"2",
            "difficulty":4,
            "id":18,
            "question":"How many paintings did Van Gogh sell in his lifetime?"}],
    "success":true,
    "total_questions":41

}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
    - Returns the id of the deleted question, success value, total questions, and questions list based on current page number to   update the frontend. 
-Sample: `curl -X DELETE http://127.0.0.1:5000/questions/10`
```{
    "deleted":10,
    "questions":[{
        "answer":"Tom Cruise",
        "category":"5",
        "difficulty":4,
        "id":4,
        "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {"answer":"Maya Angelou",
         "category":"4",
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
         },
         {"answer":"Edward Scissorhands",
         "category":"5",
         "difficulty":3,
         "id":6,
         "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
         {"answer":"Uruguay",
          "category":"6",
          "difficulty":4,
          "id":11,
          "question":"Which country won the first ever soccer World Cup in 1930?"
          },
          {"answer":"George  Washington Carver",
          "category":"4",
          "difficulty":2,
          "id":12,
          "question":"Who invented Peanut Butter?"
          },
          {"answer":"Lake Victoria",
            "category":"3",
            "difficulty":2,
            "id":13,
            "question":"What is the largest lake in Africa?"
          },
          {"answer":"The Palace of Versailles",
           "category":"3",
           "difficulty":3,
           "id":14,
           "question":"In which royal palace would you find the Hall of Mirrors?"
           },
           {"answer":"Escher",
            "category":"2",
            "difficulty":1,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {"answer":"One",
            "category":"2",
            "difficulty":4,
            "id":18,
            "question":"How many paintings did Van Gogh sell in his lifetime?"}],
    "success":true,
    "total_questions":40

}
```

#### POST /questions
- General:
    - Creates a new question using answer, category, difficulty and question. 
    - Returns the id of the created question_id, success value, total questions, and questions list based on current page number to update the frontend. 
- Sample:`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is the nearest planet to th sun", "answer": "Mercury","difficulty": "3","category":"1"}''`
```
{
    "created":51,
    "questions":[{
        "answer":"Tom Cruise",
        "category":"5",
        "difficulty":4,
        "id":4,
        "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {"answer":"Maya Angelou",
        "category":"4",
        "difficulty":2,
        "id":5,
        "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {"answer":"Edward Scissorhands",
        "category":"5",
        "difficulty":3,
        "id":6,
        "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
        {"answer":"Uruguay",
        "category":"6",
        "difficulty":4,
        "id":11,
        "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        {"answer":"George Washington Carver",
        "category":"4",
        "difficulty":2,
        "id":12,
        "question":"Who invented Peanut Butter?"
        },
        {"answer":"Lake Victoria",
        "category":"3",
        "difficulty":2,
        "id":13,
        "question":"What is the largest lake in Africa?"
        },
        {"answer":"The Palace of Versailles",
        "category":"3",
        "difficulty":3,
        "id":14,
        "question":"In which royal palace would you find the Hall of Mirrors?"
        },
        {"answer":"Escher",
        "category":"2",
        "difficulty":1,
        "id":16,
        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {"answer":"One",
        "category":"2",
        "difficulty":4,
        "id":18,
        "question":"How many paintings did Van Gogh sell in his lifetime?"
        },
        { "answer": "Mercury",
          "category":"1",
          "difficulty": "3",
          "id":51,
          "question": "What is the nearest planet to th sun", 
        }],
    "success":true,
    "total_questions":41
    }

```

#### POST /searchs/
- General:
    - Searches for questions using search.
    - Returns success value, total questions, and questions list based on current page number to update the frontend.  
-Sample: `' curl -X POST -H "Content-Type: application/json" -d '{"search":"title"}' http://127.0.0.1:5000/searchs '`
```
{
    "questions":[
        {"answer":"Maya Angelou",
         "category":"4",
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
         },
         {"answer":"Edward Scissorhands",
         "category":"5",
         "difficulty":3,
         "id":6,
         "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"}],
    "success":true,
    "total_questions":2
    }

```
#### GET /categories/<category_id>/questions
- General:
    - Returns category id,question,success value,total questions.
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`
```
{ 
    "current_category":6,
    "questions":[ 
        {"answer":"Uruguay",
        "category":"6",
        "difficulty":4,
        "id":11,
        "question":"Which country won the first ever soccer World Cup in 1930?"
        }],
    "success":true,
    "total_questions":1}
```


#### POST/quizzes
- General:
   -Allows users to play the quiz game.
   -Request parameters are category and previous questions.
   -Returns question and success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Sports", "id": "6"}}`
```
  {
    "question":{
        "answer":"Uruguay",
        "category":"6",
        "difficulty":4,
        "id":11,
        "question":"Which country won the first ever soccer World Cup in 1930?"
        },
    "success":true}

```
## Deployment N/A

## Authors

Bahiru Yimolal authured __init__.py(backend),test_flaskr(backend) and the README File(Documention).
Majority of the project files were created by Udacity.

## Acknowledgements 
To all udacity teams: Code reviwers,sessions leaders and etc....
## Project Screenshot
![Screenshot from 2023-06-06 22-30-28](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/788b0e2e-5ed8-4867-b5ff-da02ec94b0ac)
![Screenshot from 2023-06-06 22-30-58](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/e99fde4b-d421-454b-b504-bfa4f6cb5ba6)
![Screenshot from 2023-06-06 22-31-37](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/a2fddd97-ea4d-43d9-972e-07d1a6a007e8)
![Screenshot from 2023-06-06 22-31-46](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/b554e987-5e92-420f-81f2-f0f86c064fa0)
![Screenshot from 2023-06-06 22-31-59](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/39fdadd3-ed09-4b56-a276-b78eb66374c0)
![Screenshot from 2023-06-06 22-32-47](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/f9879f32-3be4-460c-9989-9aeb47855bf7)
![Screenshot from 2023-06-06 22-33-05](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/c9b859ee-5730-4bd5-b59f-2a44af3010c6)
![Screenshot from 2023-06-06 22-33-16](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/7d7c5543-46d7-4a1e-a3ce-2df6b36c645d)
![Screenshot from 2023-06-06 22-33-47](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/f3cf50a4-3624-4378-b14f-4bcf1c70c0d0)
![Screenshot from 2023-06-06 22-33-53](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/2b96c548-e7a2-4313-a1eb-34732449c5bd)
![Screenshot from 2023-06-06 22-34-02](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/a62f997a-6e8a-46b4-88c7-13201238f71b)
![Screenshot from 2023-06-06 22-34-06](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/e6d13115-99ce-49ef-83a4-391c5a2824f7)
![Screenshot from 2023-06-06 22-34-17](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/291a47f6-4f2e-4f8a-90bd-a6b133efb825)
![Screenshot from 2023-06-06 22-34-47](https://github.com/Bahiru-Yimolal/Project-Trivia-API/assets/88880193/e572bf2b-8c56-4f7d-8ced-6fbbbc8c58e7)



