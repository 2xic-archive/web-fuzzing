from utils import *
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def parse_half_baked_url(url, netloc):
	if(url.startswith("http")):
		if not url.endswith("/") and (len(urlparse(url).path) == 0):
			return url + "/"
		return url
	elif(url[:2] == "//"):
		return "http://" + url
	elif(url.startswith("/")):
		return ("https://" + netloc + url)
	elif(url == "#"):
		return None
	return url

def html_parse_all_urls(page):
	soup = BeautifulSoup(page, 'html.parser')
	response = []
	for links in soup.findAll(href=True):
		response.append(links.get("href"))
	return response

def get_hidden_parameters(request_object):
	matches = re.findall(r'<input[^<]*name=\'[^<]*\'*>|<input[^<]*name="[^<]*"*>', request_object.text)
	paramslist = []
	for match in matches:
		found_param = match.split('name=')[1].split(' ')[0].replace('\'', '').replace('"', '')
		paramslist.append(found_param)
	return request_object.url + "?" + "=undefined&".join(paramslist) + "=undefined"

def regex_find_all_urls(page):
	return re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', page)

def get_all_urls(response, page):
	urls = []
	urls.extend(html_parse_all_urls(page))
	urls.extend(regex_find_all_urls(page))
	urls.append(get_hidden_parameters(response))

	netloc = urlparse(response.url).netloc
	results = []

	'''
		sometimes a redirect will have urls that have vulns.
		pay attention and find bugs!
	'''
	for i in response.history:
		results.append(i.url) 

	for i in urls:
		fixed = parse_half_baked_url(i, netloc)
		if(fixed == None):
			continue
		results.append(fixed)
		
	merkel = merkel_tree(results)
	return results, merkel.get_hash()

def return_urls(url):
	response, page = requests_url(url)
	return get_all_urls(response, page)

