from datetime import datetime

class Company(object):
	"""An individual company with Glassdoor reviews.
	
	"""

	def __init__(self, name, website=None, logo=None, ratings=None, reviews=None):
		"""Constructor for Review object.

		Args:
			name (str): Company name
			website (Optional[str]): Company website URL
			logo (Optional[str]): Company logo URL
			ratings (Optional[Rating]): Company rating
			reviews (Optional[[Review]]): Company reviews

		"""

		self.name = name
		# check empty
		if website is None:
			# provide default value
			self.website = 'www.' + name + '.com' # possible website URL
		else:
			self.website = website
		
		# unable to provide default viable values
		self.logo = logo
		self.ratings = ratings

		# check empty
		if reviews is None:
			self.reviews = []
		else:
			self.reviews = reviews


class Rating(object):
	"""An individual 'set' of ratings from Glasdoor for a company.

	"""

	# Min and max rating
	DEFAULT_MIN_RATING, DEFAULT_MAX_RATING = 0, 5

	def __init__(self, cultureAndValues=0, seniorLeadership=0, compensationAndBenefits=0, careerOpportunities=0, workLifeBalance=0):
		"""Constructor for Rating object.

		Args:
			cultureAndValues (Optional[int]): Rating (0-5)
			seniorLeadership (Optional[int]): Rating (0-5)
			compensationAndBenefits (Optional[int]): Rating (0-5)
			careerOpportunities (Optional[int]): Rating (0-5)
			workLifeBalance (Optional[int]): Rating (0-5)

		"""

		self.cultureAndValues = cultureAndValues
		self.seniorLeadership = seniorLeadership
		self.compensationAndBenefits = compensationAndBenefits
		self.careerOpportunities = careerOpportunities
		self.workLifeBalance = workLifeBalance



class Review(object):
	"""An individual Glassdoor interview review.

	"""

	DEFAULT_DATE_FORMAT = '%b %d, %Y' # default date format specifier


	def __init__(self, role, gotOffer, experience, difficulty, length, details, date=None, questions=None):
		"""Constructor for Review object.

		Args:
			date (str): Date of review
			role (str): Role/position interviewed, e.g. 'Software Engineer'
			gotOffer (str): Status of offer, e.g. 'No Offer, Accepted Offer, Declined Offer'
			experience (str): Sentiment of experience, e.g. 'Negative Experience, Neutral Experience, Positive Experience'
			difficulty (str): Sentiment of difficulty, e.g. 'Hard Interview, Easy Interview, Average Interview'
			length (str): Length of interview process, e.g. '1 day, 4 weeks'
			details (str): Details of interview
			questions (list): Questions asked during interview
			
		"""

		# check for empty
		if date is None:
			self.date = datetime.now()
		else:
			try:
				self.date = datetime.strptime(date, Review.DEFAULT_DATE_FORMAT)
			except ValueError:
				print 'Date cannot be deserialized. Check format'
				raise

		self.role = role
		self.gotOffer = gotOffer
		self.experience = experience
		self.difficulty = difficulty
		self.length = length
		self.details = details

		# check for empty
		if questions is None:
			self.questions = []
		else:
			self.questions = questions
