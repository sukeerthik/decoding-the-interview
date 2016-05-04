import json, requests, pymongo, sys
from pymongo import MongoClient

# constants
DEFAULT_PARTNER_ID = 63896
DEFAULT_API_KEY = 'hu3pjN83MT5'
DEFAULT_REQUEST_URL = 'http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=' + str(DEFAULT_PARTNER_ID) + '&t.k=' + DEFAULT_API_KEY + '&action=employers&q='
DEFAULT_USER_AGENT = 'Mozilla/5.0'

def getGlassdoorCompanyInfo(name=None, debug=False):
	"""
	Gets the Glassdoor company info using the Glassdoor API.

	Company info is returned as JSON (dict).

	Args:
		name (str): The name of company
		debug (bool): Whether to display debugging info

	"""

	# check for empty name
	if name is None:
		return None

	# build request
	url = DEFAULT_REQUEST_URL + name
	header = {'user-agent': DEFAULT_USER_AGENT}

	# make request
	response = requests.get(DEFAULT_REQUEST_URL + name, headers=header)

	try:
		json_response = response.json()
	except ValueError:
		print 'Could not convert response as valid JSON.'
		raise

	# log response for debugging
	if debug:
		print 'Status: {}\n{}'.format(response.status_code, json_response)

	# OK
	if response.status_code == 200:
		return json_response
	# NOT OK
		return None


# run from command line
if __name__ == '__main__':
	
	# get args (company name) and make single request
	if len(sys.argv) > 1:
		name = sys.argv[1]
		debug = sys.argv[2] == 'True'

		getGlassdoorCompanyInfo(name, debug)
	else:
		print 'Usage: python data_operations.py [name (str)] [debug (str)]'



