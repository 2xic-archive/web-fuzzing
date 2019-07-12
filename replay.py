import requests
from urllib.parse import urlencode
from db import *
import json


'''
	you usally want to be able to login to a website to make the scraper
	super effective.
'''

connect = database()

url, data = connect.get_login("%URL%")
data = urlencode(json.loads(data))

response = requests.post(url, data=data, headers={
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded"
}).text

print(response)