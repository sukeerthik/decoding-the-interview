from flask import Flask, json, url_for, request
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from pymongo import MongoClient

# Globals

# MongoDB
DEFAULT_MONGO_CLIENT = MongoClient('mongodb://admin:sugarcub3d@ds011872.mlab.com:11872/dti')
DEFAULT_MONGO_DATABASE = DEFAULT_MONGO_CLIENT.dti
# collections
DEFAULT_COMPANIES_COLLECTION = DEFAULT_MONGO_DATABASE.companies
DEFAULT_ANALYSIS_COLLECTION = DEFAULT_MONGO_DATABASE.analysis
DEFAULT_REVIEWS_COLLECTION = DEFAULT_MONGO_DATABASE.reviews


# Flask
app = Flask(__name__)

@app.route('/api')
def show_api_disclaimer():
	# return a list of valid URLs for the API
	response = 'Decoding the Interview API. See below for useful URLs. <br />Companies: {}<br />Company by ID: {}<br />Reviews: {}<br />Review by ID: {}<br />Analysis: {}<br />Analysis by ID: {}'.format(url_for('get_companies'),
		url_for('get_company_info', company_id='company_id'), url_for('get_reviews'), url_for('get_review_info', review_id='review_id'), url_for('get_analysis'), url_for('get_analysis_info', analysis_id='analysis_id'))
	
	return response

# Company

@app.route('/api/companies')
def get_companies():
	# get query parameters
	query_params = request.args.to_dict()

	q_filter, q_limit, q_skip = None, 0, 0
	if 'filter' in query_params:
		q_filter = loads(query_params['filter'])
	if 'limit' in query_params:
		q_limit = int(query_params['limit'])
	if 'skip' in query_params:
		q_skip = int(query_params['skip'])

	# get objects from Mongo
	companies = [company for company in DEFAULT_COMPANIES_COLLECTION.find(filter=q_filter, skip=q_skip, limit=q_limit)]	

	# convert BSON to JSON and return
	companies_list = [dumps(company) for company in companies]
	return json.jsonify({'data': companies_list})


@app.route('/api/companies/<company_id>')
def get_company_info(company_id):

	# get object from Mongo
	company = DEFAULT_COMPANIES_COLLECTION.find_one({'_id': ObjectId(company_id)})

	# check for None
	if company:
		return json.jsonify({'data': dumps(company)})
	# company not found
	return 'Company not found. Check the ID.'
	

# Review

@app.route('/api/reviews')
def get_reviews():
	# get query parameters
	query_params = request.args.to_dict()

	q_filter, q_limit, q_skip = None, 0, 0
	if 'filter' in query_params:
		q_filter = loads(query_params['filter'])
	if 'limit' in query_params:
		q_limit = int(query_params['limit'])
	if 'skip' in query_params:
		q_skip = int(query_params['skip'])

	# get objects from Mongo
	reviews = [review for review in DEFAULT_REVIEWS_COLLECTION.find(filter=q_filter, skip=q_skip, limit=q_limit)]	

	# convert BSON to JSON and return
	reviews_list = [dumps(review) for review in reviews]
	return json.jsonify({'data': reviews_list})

@app.route('/api/reviews/<review_id>')
def get_review_info(review_id):
	# get object from Mongo
	review = DEFAULT_REVIEWS_COLLECTION.find_one({'_id': ObjectId(review_id)})

	# check for None
	if review:
		return json.jsonify({'data': dumps(review)})
	# Review not found
	return 'Review not found. Check the ID.'

# Analysis

@app.route('/api/analysis')
def get_analysis():
	# get query parameters
	query_params = request.args.to_dict()

	q_filter, q_limit, q_skip = None, 0, 0
	if 'filter' in query_params:
		q_filter = loads(query_params['filter'])
	if 'limit' in query_params:
		q_limit = int(query_params['limit'])
	if 'skip' in query_params:
		q_skip = int(query_params['skip'])

	# get objects from Mongo
	analysis = [analysis_obj for analysis_obj in DEFAULT_ANALYSIS_COLLECTION.find(filter=q_filter, skip=q_skip, limit=q_limit)]	

	# convert BSON to JSON and return
	analysis_list = [dumps(analysis_obj) for analysis_obj in analysis]
	return json.jsonify({'data': analysis_list})

@app.route('/api/analysis/<analysis_id>')
def get_analysis_info(analysis_id):
	# get object from Mongo
	analysis = DEFAULT_ANALYSIS_COLLECTION.find_one({'_id': ObjectId(analysis_id)})

	# check for None
	if analysis:
		return json.jsonify({'data': dumps(analysis)})
	# Analysis not found
	return 'Analysis not found. Check the ID.'


if __name__ == '__main__':
	app.run(debug=True)