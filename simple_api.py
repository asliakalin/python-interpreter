# A very simple Flask Hello World app for you to get started with...
# This code lives at https://asliakalin.pythonanywhere.com

from flask import Flask
from flask import request
import json
import time

app = Flask(__name__)

@app.route('/', methods =['GET', 'POST'])
def handle_request():
    text = str(request.args.get('input')) # Requests the < ...url... ?input= a > ==> input will be the query word we'll be searching for when we make a request
    character_count = len(text)

    # create a dataset or json format
    data_set = {'input':text, 'timestamp': time.time(), 'character_count': character_count} # a map of values we will insert
    # change the dataset into a json
    json_dump = json.dumps(data_set)
    # return json data
    return json_dump