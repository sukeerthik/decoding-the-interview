import json
from glob import glob
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

# Options
NUM_TRAINING_FILES = 100
TRAINING_DATA_PATH = "./training_data/"

################################################

training_data = []

test = [
    ('the beer was good.', 'pos'),
    ('I do not enjoy my job', 'neg'),
    ("I ain't feeling dandy today.", 'neg'),
    ("I feel amazing!", 'pos'),
    ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]

################################################

def obj_dict(obj):
    return obj.__dict__
#enddef

def get_text_from_file(keyword, tag):
  path = TRAINING_DATA_PATH + tag + '/'
  fileName = glob(path + keyword + "*.txt")[0] # finds the full name of file starting with the keyword 'cv###'
  with open(fileName, 'r') as f:
  	data = f.read()
  	return data
  #endwith
#enddef

def export_training_data_to_json():
	jsonFile = open("training_data.json", 'w')
	jsonFile.write(json.dumps(training_data, indent=4, separators=(',', ': '), default=obj_dict))
	jsonFile.close()
#enddef

def aggregate_sentiment_data(tag):
  for i in range (NUM_TRAINING_FILES):
    num = format(i, "03") # fills 0s in front until three digits
    text = get_text_from_file("cv" + num, tag)
    training_data.append({"text" : text, "label": tag})
  #endfor
#enddef

def train_data():
  with open("training_data.json", 'r') as f:
    nbayes = NaiveBayesClassifier(f, format="json") # I think training from JSON is faster
    return nbayes
  #endwith
#enddef

def run_naive_bayes():
  print "# Aggregating positive sentiment text data ..."
  aggregate_sentiment_data("pos")
  print "# Aggregating negative sentiment text data ..."
  aggregate_sentiment_data("neg")
  print "# Exporting data to JSON ..."
  export_training_data_to_json()
  print "# Training Naive Bayes Classifier ..."
  nbayes = train_data()
#enddef

################################################

if __name__ == "__main__":
  run_naive_bayes()
#endif