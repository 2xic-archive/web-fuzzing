
from db import *
from parser import *
import time
from utils import *


connect = database()

def bootstrap(url, parrent_url=None):
	global connect
	if(parrent_url == None):
		parrent_url = url
		'''
			this indiactes that it's a bootstrap url.
		'''
	urls, merkel_hash = return_urls(url)
	print(merkel_hash)

	if not connect.check_insert_hash(merkel_hash):
		for url in urls:
			try:
				connect.insert_url(url, parrent_url)
			except Exception as e:
				print(e)
				print((url, parrent_url))
				print("")
		print("Unique urls")
	else:
		print("Already added!")
	connect.now_scanned(url)

for i in scope:
	bootstrap("https://" + i)

for i in connect.not_scanned():
	if not validate_scope(i[0]):
		continue
	print(i[0])
	bootstrap(i[0], i[0])
	time.sleep(3)
