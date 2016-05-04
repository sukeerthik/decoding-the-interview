import json, requests, pymongo, sys
from pymongo import MongoClient

# constants
DEFAULT_PARTNER_ID = 63896
DEFAULT_API_KEY = 'hu3pjN83MT5'
DEFAULT_REQUEST_URL = 'http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=' + str(DEFAULT_PARTNER_ID) + '&t.k=' + DEFAULT_API_KEY + '&action=employers&q='
DEFAULT_USER_AGENT = 'Mozilla/5.0'

# file IO
DEFAULT_COMPANY_LIST_FILENAME = 'full_company_list.txt'
DEFAULT_REVIEW_FOLDER = './company_data/'

# MongoDB
DEFAULT_MONGO_CLIENT = MongoClient('mongodb://admin:sugarcub3d@ds011872.mlab.com:11872/dti')
DEFAULT_MONGO_DATABASE = DEFAULT_MONGO_CLIENT.dti


def getCompanyList(file_name=None):
	"""
	Get list of companies to get data for. Reads from a file.

	Args:
		file_name (str): Name of file with list of companies
	"""

	# check empty
	if file_name is None:
		return None

	# get list of company names
	with open(file_name) as f:
		names = [name.replace('\n', '') for name in list(f)]

	return names

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

	# OK - return company info
	if response.status_code == 200:
		# extract correct company info
		employer_list = json_response['response']['employers']

		if len(employer_list) > 0:
			for i in range(len(employer_list)):
				if employer_list[i]['exactMatch']:
					return employer_list[i]
		else:
			return None

	# NOT OK
		return None

def getAllCompaniesInfo(name_list=None):
	"""
	Gets the Glassdoor company info for all companies in a given list. Returns a list of dicts containing respective company info.

	Args:
		name_list (list): List of company names.

	"""

	if name_list is None:
		return None

	# build list of company infos 
	companies_info = [getGlassdoorCompanyInfo(name) for name in name_list]

	return companies_info

def getCompanyReviews(name=None):
	"""
	Gets the reviews for a specific company. Returns list of reviews.

	Args:
		name (str): Company to get reviews for.
	"""

	# check empty
	if name is None:
		return None

	# open file for reading
	with open(DEFAULT_REVIEW_FOLDER + name.lower().replace(' ', '').strip() + '.json') as f:

		reviews = json.load(f)
		return reviews
		


"""MongoDB operations """
def buildCompanyCollection(company_list_filename=DEFAULT_COMPANY_LIST_FILENAME):
	"""
	Builds the collection of companies in MongoDB and returns their ids in a list.

	Args:
		db_instance (Mongo database object)
	"""

	# get collection
	companies = DEFAULT_MONGO_DATABASE.companies

	# get company info objects to insert
	company_list = getCompanyList(company_list_filename)
	companies_info = getAllCompaniesInfo(company_list)

	# clean all company objects
	cleaned_companies = [cleanCompany(company) for company in companies_info]

	# insert cleaned companies
	result = companies.insert_many(cleaned_companies)

	# return their object IDs assigned by Mongo
	return result.inserted_ids

def buildReviewCollection(company_ids=None, company_list_filename=DEFAULT_COMPANY_LIST_FILENAME):
	"""
	Builds the collection of reviews in MongoDB and assigns the company ID to each review for its respective company.
	Assumes company list and company ids are 1:1 order

	Args:
		company_ids (list): List of company IDs (ObjectId)
		company_list (list): List of company names
	"""
	# get company list
	company_list = getCompanyList(company_list_filename)
	
	# check empty or for any mismatch in IDs and company list
	if company_ids is None or company_list is None or len(company_ids) != len(company_list):
		return None

	# get collection
	reviews = DEFAULT_MONGO_DATABASE.reviews

	# list of lists of review IDs
	reviews_ids = []

	# insert formatted reviews
	for i in range(len(company_list)):
		# curr company
		company = company_list[i]
		
		# get reviews and add company ID
		orig_reviews = getCompanyReviews(company)
		for r in orig_reviews:
			r['companyId'] = company_ids[i]

		# insert into Mongo and get IDs of inserted reviews
		reviews_ids.append(reviews.insert_many(orig_reviews).inserted_ids)

	
	# return list of lists of review IDs
	return reviews_ids



def cleanCompany(company=None):
	"""
	Cleans a company object (dict) and returns cleaned version.

	Args:
		company (dict): Dict of the company object.

	"""
	# check empty
	if company is None:
		return None

	# make copy
	cleaned_company = dict(company)

	# remove unwanted fields
	if 'id' in cleaned_company:
		del cleaned_company['id']
	if 'exactMatch' in cleaned_company:
		del cleaned_company['exactMatch']
	if 'isEEP' in cleaned_company:
		del cleaned_company['isEEP']
	if 'sectorId' in cleaned_company:
		del cleaned_company['sectorId']
	if 'featuredReview' in cleaned_company:
		del cleaned_company['featuredReview']
	if 'industryId' in cleaned_company:
		del cleaned_company['industryId']
	if 'ratingDescription' in cleaned_company:
		del cleaned_company['ratingDescription']
	if 'industryName' in cleaned_company:
		del cleaned_company['industryName']

	return cleaned_company


# run from command line
if __name__ == '__main__':
	print 'hi'

