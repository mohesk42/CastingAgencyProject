# Casting Agency Project

Casting Agency API is used to by several types of users to manage and view movies and actors.

This API has 3 types of users:

1. Assistant
2. Director
3. Executive Producer 

## URL
1. Heroku:
2. Localhost: localhost:5000

## To start the server

Use the following commands to create the database 
```
flask run
```
Then you can use the link provided in the output.


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns all categories of the questions.
 
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET /questions
- General:
    - Returns list of questions paginated in group of 10.
    - list of categories
    - total number of questions
 
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "all",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 26
}
```

#### GET '/categories/<id>/questions'
- General:
    - Returns list of questions of the specifed category.
    - current category.
    - total number of questions in the category.
 
- Sample: `curl http://127.0.0.1:5000/categories/5/questions`

```
{
  "currentCategory": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```

#### DELETE '/questions/<id>'
- General:
    - Delete a question.
    - return success status.
 
- Sample: `curl http://127.0.0.1:5000/questions/8 -X DELETE`

```
{
    "success": true,
    "deleted": 8
}
```

#### POST '/search_questions'
- General:
    - Search questions by given search term.
    - return list of questions.
    - total number of questions found.
 
- Sample: `curl http://127.0.0.1:5000/search_questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "world"}'`

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

#### POST '/questions'
- General:
    - create new question.
    - return sucess status
 
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the tallest tower in the world?", "answer": "Khalifa tower", "difficulty": 2, "category": "2" }'`

```
{
  "success": true
}
```
#### POST '/quizzes'
- General:
    - Get random question from category of the quiz.
    - Return question not provided in the previous questions list.
 
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 6], "quiz_category": {"type": "Art", "id": "2"}}'`

```
{
  "question": {
    "answer": "ee",
    "category": 2,
    "difficulty": 1,
    "id": 29,
    "question": "dfdf"
  },
  "success": true
}
```