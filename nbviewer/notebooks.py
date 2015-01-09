import os, time
import urllib2
import json
import requests
from .redisclient import  getUserName

def get_notebooks(nb_url, user_id=None, public=False):
	notebooks = []
	if user_id is not None:
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
	elif public:
		headers = {'content-type': 'application/json'}
		url = nb_url + "/api/notebooks/public"
		try:
			r = requests.get(url,headers=headers)
			for nb in r.json():
			 if nb['type'] == "notebook":
			 	nb['published_by'] = getUserName(nb['name'].split("_")[0])
			 	nb['path'] += "/" + nb['name']
			 	nb['presentation_name'] = "_".join(nb['name'].split("_")[1:])
			 	notebooks.append(nb)
		except:
			return notebooks
	return notebooks

def get_notebook_info(nb_url, path):
	notebook = {}
	headers = {'content-type': 'application/json'}
	url = nb_url + "/api/notebooks/" + path
	try:
		r = requests.get(url,headers=headers)
		return r.json()
	except:
		return notebook
	return notebook

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

def publish_notebook(nb_url, src_path, nb_name):
	try:
		headers = {'content-type': 'application/json'}
		notebook = get_notebook_info(nb_url, src_path)
		nb_name = src_path.split("/")[0] + "_" + nb_name
		if nb_name.endswith('.ipynb'): nb_name += ".ipynb"
		upload_notebook(nb_url, "public", nb_name, 
			json.dumps(notebook['content']))
	except:
		return

def delete_notebook(nb_url, path, nb_name):
	headers = {'content-type': 'application/json'}
	body = {}
	url = nb_url + "/api/notebooks/" + path + "/" + nb_name
	try:
		r = requests.delete(url,headers=headers)
		return True
	except:
		return False