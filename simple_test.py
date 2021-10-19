import requests as rq
from datetime import datetime

# comes from pythonanywhere web app url
BASE_URL = "https://asliakalin.pythonanywhere.com"

# for the requests module:
payload = {'input': 'TRYING OUT THE API!'}  # for the query of input(s), we will insert what input we want to put insert ==> params
response = rq.get(BASE_URL, params=payload)

# response we got from the url
json_values = response.json() # response --> must convert to json

# get values for each param key
rq_input = json_values['input']
timestamp = json_values['timestamp']
character_count = json_values['character_count'] # char count of the text we inserted in payload

print(f'Input is: {rq_input}')
print(f'Date is: {datetime.fromtimestamp(timestamp)}')
print(f'Char count is: {character_count}')
