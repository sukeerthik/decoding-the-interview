import sys, json, Analysis 
from glob import glob
from stop_words import get_stop_words
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

class CompanyAnalyzer(object):
	"""A wrapper to the TextBlob library customized for analyzing Glassdoor companies.

	"""

	