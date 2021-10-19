# Python Interpreter

## A. PythonAnywhere
Here is the steps I followed while writing my own python interpreter api.
### 1. Create a new project, in the project directory:
create < api.py >
### 2. To handle http requests in python, in the terminal:
pip install requests
### 3. Go to pythonanywhere.com and create an account (can be beginner account). After sign up, go to "Open up Web App" section and make a new web app
now there is a server running at asliakalin.pythonanywhere.com, currently just displays "hello from Flask!" --> we want to change that to give us some json data
### 4. Go to source code to change the code:
Code > Source code > Go to directory > flask_app.py


## B. Testing the API: Built in Debugging & Web Server for Development
- run with ```python3 api.py``` to start the debugging mode
- will show ```"Running on http://127.0.0.1:8000/"```
- in another window, run 
    - ```curl -v http://127.0.0.1:8000/tester``` to send a get request
    - more complicated requests: ```curl -H "Content-Type: application/json" -X POST -d '{"inputs": [1,2,3], "solutions":[0,2,4], "code": "outputs=inputs*2"}' http://127.0.0.1:8000/tester```





## C. A Restful API:
- flask has content type as html (not json as we'd expect from a REST API) 
- use ```from flask import jsonify``` to get json data and convert content type to ```application/json```
