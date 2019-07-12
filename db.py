
import psycopg2
from metrics import *

class database:
	def __init__(self):
		self.conn = psycopg2.connect(dbname="bugs", 
								user = "postgres", 
								password = "newPassword", 
								host = "localhost", port = "5432",
								connect_timeout = 10)

		self.cursor = self.conn.cursor()		
		self.boot()
		print("Done booting")

	def boot(self):
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
							url text  NOT NULL PRIMARY KEY,
							parrent text,
							scanned INT,
							score INT
					);''')

		self.cursor.execute('''CREATE TABLE IF NOT EXISTS hashes (
							hash text NOT NULL PRIMARY KEY
					);''')
		
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS login (
							url text NOT NULL PRIMARY KEY,
							data text
					);''')
		self.commit()

	def insert_login(self, url, data):
		try:
			self.cursor.execute('INSERT INTO login (url, data) VALUES (%s,%s)' , (url, data))
			self.commit()
		except Exception as e:
			self.conn.rollback()
			if not "duplicate key value" in str(e):
				print(e)
			elif("duplicate key value" in str(e)):
				#	guess you want to update?
				self.cursor.execute('UPDATE login SET data=%s WHERE url=%s' , (data, url))
				self.commit()


	def get_login(self, url):
		self.cursor.execute("SELECT url, data FROM login where url LIKE %s", (url, ))
		response = self.cursor.fetchall()
		if(len(response) == 0):
			self.cursor.execute("SELECT url, data FROM login where strpos(%s, url) > 0", (url, ))
			response = self.cursor.fetchall()
			if(len(response) == 0):
				return None
			return response[0]	
		return response[0]
		
	def check_insert_hash(self, merkel_hash):
		self.cursor.execute("SELECT * FROM hashes where hash=%s", (merkel_hash, ))
		if(len(self.cursor.fetchall()) == 0):
			self.insert_hash(merkel_hash)
			return False
		return True

	def not_scanned(self):
		self.cursor.execute("SELECT url FROM urls where scanned=0")
		return self.cursor.fetchall()

	def now_scanned(self, url):
		self.cursor.execute("UPDATE urls SET scanned=1 WHERE url=%s", (url, ))
		self.commit()

	def update_score(self, url, new_score):
		self.cursor.execute("UPDATE urls SET score=%s WHERE url=%s", (url, new_score))
		self.commit()

	def insert_hash(self, merkel_hash):
		self.cursor.execute("INSERT INTO hashes (hash) VALUES (%s)" , (merkel_hash, ))
		self.commit()

	def insert_url(self, url, parrent):
		try:
			self.cursor.execute('INSERT INTO urls (url, parrent, scanned, score) VALUES (%s,%s,%s, %s)' , (url, parrent, 0, inital_score(url, parrent)))
			self.commit()
		except Exception as e:
			self.conn.rollback()
			if not "duplicate key value" in str(e):
				print(e)

	def custom_query(self, query, page=0):
		try:
			self.cursor.execute('SELECT url FROM urls where url LIKE %s LIMIT 10 OFFSET %s ORDER BY score DESC;' , (query, page * 10,))
			return self.cursor.fetchall()
		except Exception as e:
			print(e)

	def commit(self):
		self.conn.commit()
