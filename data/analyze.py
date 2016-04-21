import json
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

# Options
fileName = "yahoo.json"

companyName = fileName[:-5]

################################################

# Keywords to remove from noun phrase analysis
removeThese = [companyName, "phone", "interview", "hr", "got", "applied", "overall", "engineer", "met", "was", "went"]

################################################


def print_stats(data, blob_d, blob_q):
  print "# Calculating sentiment ..."
  polarity = round(blob_d.sentiment.polarity, 5)
  subjectivity = round(blob_d.sentiment.subjectivity, 5)
  print "# Enumerating top noun phrases ..."
  phrases = get_top_phrases(blob_d)
  print "# Discovering interview question keywords ..."
  keywords = get_top_phrases(blob_q)
  print "# Finding the most positive and negative review ..."
  reviews = get_top_reviews(data)
  print "\n" + companyName.upper()
  print ""
  print "Overall Sentiment Score: " + str(polarity)
  print "Overall Subjectivity Score: " + str(subjectivity)
  print ""
  print "Most Positive Interview Review:"
  print "Sentiment Score: " + str(round(reviews[0][1], 5))
  print reviews[0][0]
  print ""
  print "Most Negative Interview Review:"
  print "Sentiment Score: " + str(round(reviews[1][1], 5))
  print reviews[1][0]
  print ""
  print "Most Frequent Phrases:"
  ctr = 1
  for p in phrases:
    if (ctr > 25):
      break
    #endif
    print str(ctr) + ". " + p[0]
    ctr+=1
  #endfor
  print ""
  print "Top Interview Question Keywords:"
  ctr = 1
  for k in keywords:
    if (ctr > 25):
      break
    #endif
    print str(ctr) + ". " + k[0]
    ctr+=1
  #endfor
  print ""
#enddef

################################################

def get_data_from_json(fileName):
  with open(fileName) as json_file:
    json_data = json.load(json_file)
    return json_data
#enddef

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

def get_top_phrases(blob):
  np_freq = get_noun_phrases(blob)
  np_freq_scrubbed = np_freq[:]
  for n in np_freq:
    if (any(x in n[0] for x in removeThese)):
    	np_freq_scrubbed.remove(n)
    #endif
  #endfor
  return np_freq_scrubbed
#enddef

# Not useful
def get_all_ngrams(blob, num):
  return blob.ngrams(n=num)
#enddef

def get_word_counts(blob):
  word_counts = blob.word_counts
  word_counts_sorted = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
  return word_counts_sorted
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
  return [(posReview, posVal), (negReview, negVal)]
#enddef

################################################

if __name__ == "__main__":
  data = get_data_from_json(fileName)
  details_text = get_text_from_data(data, "details")
  questions_text = get_text_from_data(data, "questions")
  blob_details = TextBlob(details_text)
  blob_questions = TextBlob(questions_text)
  print_stats(data, blob_details, blob_questions)
#endif