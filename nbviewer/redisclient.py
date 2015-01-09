import redis
import json
import hashlib

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

def setUserId(username):
	r = redis.Redis(connection_pool=POOL)
	userid = hashlib.sha256(username.encode()).hexdigest() 
	r.hset('users', username, userid)
	r.hset('users', userid, username)
	return userid

def getUserId(username):
	r = redis.Redis(connection_pool=POOL)
	userid = r.hget('users', username)
	if userid is None:
		return setUserId(username)
	return userid

def getUserName(userid):
	r = redis.Redis(connection_pool=POOL)
	username = r.hget('users', userid)
	return username

def getNoteBooks(userid):
	r = redis.Redis(connection_pool=POOL)
	notebooks = r.hget('user:'+str(userid), 'notebooks')
	if notebooks is None: return []
	elif isinstance(notebooks, str):return eval(notebooks)

def appendNoteBook(userid, notebook):
	r = redis.Redis(connection_pool=POOL)
	notebooks = getNoteBooks(userid)
	if notebook not in notebooks:notebooks.append(notebook)
	return r.hset('user:'+str(userid), 'notebooks', json.dumps(notebooks))