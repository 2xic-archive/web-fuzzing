import requests
from urllib.parse import urlparse
import hashlib
import sys, os
from configs import *

def requests_url(url, type_request="GET"):

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
	}

	response = None
	if(type_request == "GET"):
		response = requests.get(url, headers=headers)
	else:
		pass

	return response, response.text

def validate_scope(url, predefined=None):
	if(url == None):
		return False
	if(predefined == None):
		predefined = scope

	url_netloc = urlparse(url).netloc
	for url in predefined:
		if(url in url_netloc):
			return True
	return False

def parse_parameters(url):
	key = []
	value = []
	
	found_question_mark = False
	key_or_value = 0
	look_aside_buffer = ""

	for i in range(len(url)):
		if(url[i] == "?"):
			found_question_mark = True
		elif(url[i] == "&"):
			value.append(look_aside_buffer)
			key_or_value = 0
			look_aside_buffer = ""
		elif(url[i] == "="):
			key.append(look_aside_buffer)
			look_aside_buffer = ""
			key_or_value = 1
		elif(found_question_mark):
			look_aside_buffer += url[i]

	if(key_or_value == 0):
		key.append(look_aside_buffer)
	elif(key_or_value == 1):
		value.append(look_aside_buffer)
	return key, value

def catch_exception():
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(exc_type, fname, exc_tb.tb_lineno)

class node:
	def __init__(self, content):
		self.hash =	hashlib.sha256(content.encode()).hexdigest()
		self.parrent = None

	def __str__(self):
		return self.hash

	def __add__(self, other):
		return self.hash + other.hash

class merkel_tree:
	def __init__(self, data):
		self.data = data
		self.leafs = []

		for i in data:
			self.leafs.append(node(i))

		self.root = self.grow_tree()

	def get_hash(self):
		return self.root.hash

	def grow_tree(self, working_leaf=None):
		if(working_leaf == None):
			working_leaf = self.leafs

		size = len(working_leaf)
		if(size == 1):
			return working_leaf[0]
		if(size == 0):
			return node("")

		new_leafs = []
		for i in range(0, size, 2):
			left = working_leaf[i]
			right = node("")
			if((i + 1) < size):
				right = working_leaf[i + 1]

			new_leafs.append(self.combine_leaf(left, right))
		return self.grow_tree(new_leafs)

	def combine_leaf(self, left, right):
		combined_leaf = node(left + right)
		left.parrent = combined_leaf
		right.parrent = combined_leaf
		return combined_leaf
