class Analysis:

  def __init__(self, pattern_sentiment, pattern_subjectivity, overall_sentiment, pos_sentiment, neg_sentiment, top_details_nphrases, top_questions_nphrases, most_positive_review, most_negative_review):
    self.pattern_sentiment = pattern_sentiment
    self.pattern_subjectivity = pattern_subjectivity
    self.overall_sentiment = overall_sentiment
    self.pos_sentiment = pos_sentiment
    self.neg_sentiment = neg_sentiment
    self.top_details_nphrases = top_details_nphrases
    self.top_questions_nphrases = top_questions_nphrases
    self.most_positive_review = most_positive_review
    self.most_negative_review = most_negative_review
  #enddef

#endclass