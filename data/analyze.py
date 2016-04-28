import json
import Analysis
from glob import glob
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

################################################
# Options
################################################

NUM_TRAINING_FILES = 100 # Cornell movie review set goes up to 1000
TRAINING_DATA_PATH = "./training_data/"
COMPANY_DATA_PATH = "./company_data/"
COMPANY_LIST_PATH = "./company_list.txt"

################################################
# Global Data
################################################

COMPANY_LIST = []
COMPANY_LIST_KEYWORDS = []

# Keywords to remove from noun phrase analysis
# TODO: add company name to this on the fly
REMOVE_KEYWORDS = ["phone", "interview", "hr", "got", "applied", "overall", "engineer", "met", "was", "went"]

################################################
# I/O and File Functions
################################################

def obj_dict(obj):
  return obj.__dict__
#enddef

def update_company_list():
  with open(COMPANY_LIST_PATH) as f:
    for line in f:
      company = line.replace('\n', '')
      company_keyword = company.strip().replace(' ', '').lower()
      COMPANY_LIST.append(company)
      COMPANY_LIST_KEYWORDS.append(company_keyword)
  	#endfor
  #endwith
#enddef

def get_data_from_json(fileName):
  with open(fileName) as json_file:
    json_data = json.load(json_file)
    return json_data
#enddef

def get_text_from_file(keyword, tag):
  path = TRAINING_DATA_PATH + tag + '/'
  fileName = glob(path + keyword + "*.txt")[0] # finds the full name of file starting with the keyword 'cv###'
  with open(fileName, 'r') as f:
  	data = f.read()
  	return data
  #endwith
#enddef

def export_training_data_to_json(data):
  jsonFile = open("training_data.json", 'w')
  jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
  jsonFile.close()
#enddef

def export_analysis_data_to_json(data, companyName):
  jsonFile = open(companyName + "_analysis.json", 'w')
  jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
  jsonFile.close()
#enddef

################################################
# Training the Naive Bayes Classifier
################################################

def aggregate_sentiment_data(data, tag):
  for i in range (NUM_TRAINING_FILES):
    num = format(i, "03") # fills 0s in front until three digits
    text = get_text_from_file("cv" + num, tag)
    data.append({"text" : text, "label": tag})
  #endfor
  return data
#enddef

def train_nbayes():
  with open("training_data.json", 'r') as f:
    nbayes = NaiveBayesClassifier(f, format="json") # I think training from JSON is faster
    return nbayes
  #endwith
#enddef

def train_classifier():
  print "# Aggregating positive sentiment text data ..."
  data = aggregate_sentiment_data([], "pos")
  print "# Aggregating negative sentiment text data ..."
  data = aggregate_sentiment_data(data, "neg")
  print "# Exporting training data as \"training_data.json\" ..."
  export_training_data_to_json(data)
  print "# Training Naive Bayes Classifier ..."
  nbayes = train_nbayes()
  return nbayes
#enddef

################################################
# Blob Analysis
################################################

def get_text_from_data(data, tag):
  textData = ""
  if (tag == "details"):
    for review in data:
      textData = textData + review[tag] + " "
    #endfor
  elif (tag == "questions"):
    for review in data:
      for question in review[tag]:
        textData = textData + question + " "
      #endfor
    #endfor
  #endif
  return textData
#enddef

def get_noun_phrases(blob):
  np_freq = blob.np_counts
  np_freq_sorted = sorted(np_freq.items(), key=lambda x: x[1], reverse=True)
  return np_freq_sorted
#enddef

def get_top_phrases(blob, companyName):
  np_freq = get_noun_phrases(blob)
  np_freq_scrubbed = np_freq[:]
  removeThese = [companyName.lower()]
  for word in REMOVE_KEYWORDS: # REMOVE_KEYWORDS is global so to add the companyName we have to copy over data
    removeThese.append(word)
  #endfor
  for n in np_freq:
    if (any(x in n[0] for x in removeThese)):
      np_freq_scrubbed.remove(n)
    #endif
  #endfor
  return np_freq_scrubbed[:25] # top 25
#enddef

def get_top_reviews(data):
  posReview = data[0]
  negReview = data[0]
  posVal = 0
  negVal = 0
  for review in data:
    text = review["details"]
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if (sentiment > posVal):
      posReview = review
      posVal = sentiment
    #endif
    if (sentiment < negVal):
      negReview = review
      negVal = sentiment
    #endif
  #endfor
  return (posReview, round(posVal, 5)), (negReview, round(negVal, 5))
#enddef

def analyze_sentiment(data, classifier):
  text = get_text_from_data(data, "questions")
  prob_dist = classifier.prob_classify(text)
  overall_sentiment = prob_dist.max()
  pos_sentiment = round(prob_dist.prob("pos"), 2)
  neg_sentiment = round(prob_dist.prob("neg"), 2)
  return overall_sentiment, pos_sentiment, neg_sentiment
#enddef

def analyze_details(data, company):
  text = get_text_from_data(data, "details")
  blob = TextBlob(text)
  pattern_sentiment = round(blob.sentiment.polarity, 5)
  pattern_subjectivity = round(blob.sentiment.subjectivity, 5)
  top_details_nphrases = get_top_phrases(blob, company)
  return pattern_sentiment, pattern_subjectivity, top_details_nphrases
#enddef

def analyze_questions(data, company):
  text = get_text_from_data(data, "questions")
  blob = TextBlob(text)
  top_questions_nphrases = get_top_phrases(blob, company)
  return top_questions_nphrases
#enddef

def analyze_top_reviews(data):
  top_reviews = get_top_reviews(data)
  return top_reviews[0], top_reviews[1]
#enddef

def analyze_data(classifier):
  for i in range(len(COMPANY_LIST)):
    analyzed_data = []
    company = COMPANY_LIST[i]
    company_kw = COMPANY_LIST_KEYWORDS[i]
    print "# Analyzing " + company + " ..."
    data = get_data_from_json(COMPANY_DATA_PATH + company_kw + ".json")
    pattern_sentiment, pattern_subjectivity, top_details_nphrases = analyze_details(data, company)
    top_questions_nphrases = analyze_questions(data, company)
    overall_sentiment, pos_sentiment, neg_sentiment = "", "", "" #analyze_sentiment(data, classifier)
    most_positive_review, most_negative_review = analyze_top_reviews(data)
    a = Analysis.Analysis(pattern_sentiment, pattern_subjectivity, overall_sentiment, pos_sentiment, neg_sentiment, top_details_nphrases, top_questions_nphrases, most_positive_review, most_negative_review)
    analyzed_data.append(a)
    export_analysis_data_to_json(analyzed_data, company_kw)
  #endfor
#enddef

################################################
# Main
################################################

def init():
  update_company_list()
#enddef

if __name__ == "__main__":
  init()
  #nbayes = train_classifier()
  nbayes = ""
  analyze_data(nbayes)
#endif