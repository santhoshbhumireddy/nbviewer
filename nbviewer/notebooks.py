import os, time
import urllib2
import json
import requests
from .redisclient import  getNoteBooks

def get_notebooks(nb_url, user_id=None, public=False):
	notebooks = []
	if user_id is not None:
		#return getNoteBooks(user_id)
		headers = {'content-type': 'application/json'}
		url = nb_url + "/api/notebooks/" + user_id
		try:
			r = requests.get(url,headers=headers)
			for nb in r.json():
			 if nb['type'] == "notebook":
			 	nb['path'] += "/" + nb['name']
			 	notebooks.append(nb)
		except:
			return notebooks
	return notebooks

def get_notebook_info(nb_url, nb_name):
	data = urllib2.urlopen(nb_url)
	json_data = data.read()
	list_of_dicts = json.loads(json_data)
	for d in list_of_dicts:
		if d['name'] == nb_name:
			return d['notebook_id']
	return None

def create_notebook(nb_url, path, nb_name):
	headers = {'content-type': 'application/json'}
	body = {}
	try:
		if nb_name == '':
			url = nb_url + "/api/notebooks/" + path
			r = requests.post(url,data=json.dumps(body),headers=headers)
			return r.json()
		else:
			if not nb_name.endswith('.ipynb'): nb_name += ".ipynb"
			url = nb_url + "/api/notebooks/" + path + "/" + nb_name
			r = requests.put(url,data=json.dumps(body),headers=headers)
			return r.json()
	except:
		return False

def upload_notebook(nb_url, path, nb_name, content):
	headers = {'content-type': 'application/json'}
	body={'content':json.loads(content)}
	try:
		if nb_name == '':
			url = nb_url + "/api/notebooks/"+ path
			r = requests.post(url,data=json.dumps(body),headers=headers)
			return True
		else:
			if not nb_name.endswith('.ipynb'): nb_name += ".ipynb"
			url = nb_url + "/api/notebooks/"+ path + "/" + nb_name
			r = requests.put(url,data=json.dumps(body),headers=headers)
			return True
	except:
		return False

def delete_notebook(nb_url, path, nb_name):
	headers = {'content-type': 'application/json'}
	body = {}
	url = nb_url + "/api/notebooks/" + path + "/" + nb_name
	try:
		r = requests.delete(url,headers=headers)
		return True
	except:
		return False