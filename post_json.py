import requests
import json, sys

if __name__ == "__main__":

	# read json file into a dictionary
	with open("bio_excel.json", "r") as fjson:
		json_data = json.load(fjson)

	# get API token
	headers = {'Content-Type': 'application/json'}
	r = requests.post(
		'https://dev.bio.tools/api/rest-auth/login/', 
		data = json.dumps({ 'username' : sys.argv[1], 'password' : sys.argv[2]}),
		headers = headers
	)

	token = r.json()['key']

	# register resources
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Token ' + token
	}

	for json_data_elem in json_data:
		# try to get the resource
		r = requests.get(
			'https://dev.bio.tools/api/tool/'+json_data_elem['id'], 
			headers = headers
		)

		if r.status_code == 200:
			print 'Resource ' + json_data_elem['id'] + ' already exists. Skipping.'
			print r.text

		elif r.status_code == 404:
			print 'Not found resource ' + json_data_elem['id'] + ". Adding..."

			r = requests.post(
				'https://dev.bio.tools/api/tool/', 
				data = json.dumps(json_data_elem),
				headers = headers
			)
			print r
			if r.status_code == 400:
				print r.raise_for_status()


		



