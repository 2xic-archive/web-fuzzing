

'''
	you don't have perfect information. just indications....
'''

def inital_score(url, parrent_url):
	'''
		intital score from a page, you have minimal info.... Be cleaver
			-	url and parrent url
			-	parrent url may indicate the results of the underlaying url, but
				not necearrly.
			-	or just select a url that has a path that have been visited few times.
	'''
	return 1

def scanned_score(url, data):
	'''
		update the score after you have visited the page
			-	based on elements?	->	great if you want to send it to chrome
			-	hidden parameters found on page? vs parameters in url?
	'''
	return 2
