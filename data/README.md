# Data Analyzer for Decoding The Interview

Text analysis on company data retrieved from the [Glassdoor Interview Scraper](https://github.com/williamxie11/glassdoor-interview-scraper) for [Decoding The Interview](https://github.com/williamxie11/decoding-the-interview). 

This analysis includes sentiment analysis and noun phrase extraction using [TextBlob](http://textblob.readthedocs.io/en/dev/) as well as training a naive Bayes classifier on the [Cornell Movie Review Data Set](http://www.cs.cornell.edu/people/pabo/movie-review-data/) for further analysis.

## Installation

* Python 2.7.*

* TextBlob
```sh
$ pip install -U textblob
$ python -m textblob.download_corpora
```

## Usage

1. Modify company_list.txt with a list of the companies to analyze delimited by newlines.
2. Add company JSON data (default is company_data folder in root dir)
3. Edit the Options section of analyze.py with the path to the training data, company data, and specify the number of data points to train the classifier. Training the default 100 data points takes about fives minutes. This means 100 positive and 100 negative data points from the Cornell Movie Review Data Set.
<img src="http://i.imgur.com/GT7tNjZ.png" width="640">
4. Run the analyzer
```sh
$ python analyze.py
```

## Results

<img src="http://i.imgur.com/czovgKS.png" width="480">

The analyzer will output a JSON for each company in the root directory as [company_name]_analysis.txt.

**most_negative_review** [*Review Object*](https://github.com/williamxie11/glassdoor-interview-scraper/blob/master/Review.py) = tuple of most negative Glassdoor review (using the structure from the Glassdoor Interview Scraper) for the company using TextBlob's built-in sentiment analysis and the sentiment analysis score from range [-1, 1]

**most_positive_review** [*Review Object*](https://github.com/williamxie11/glassdoor-interview-scraper/blob/master/Review.py) = most positive Glassdoor review

**top_details_nphrases** *[(String, Int) ...]* = descending list of tuples containing the most frequent noun phrases and their frequency from the details of each interview review

**top_questions_nphrases** *[(String, Int) ...]* = descending list of tuples containing the most frequent noun phrases and their frequency from the interview questions of each review

**pattern_sentiment** *Float* = overall polarity score in range [-1, 1]

**pattern_subjectivity** *Float* = overall subjectivity score in range [-1, 1]

**pos_sentiment** *Float* = positive sentiment score from the naive Bayes classifier

**neg_sentiment** *Float* = negative sentiment score from the naive Bayes classifier

**overall_sentiment** *String* = a "pos" or "neg" denoting the general sentiment over all reviews

