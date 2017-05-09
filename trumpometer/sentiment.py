##
# vader: http://www.aaai.org/ocs/index.php/ICWSM/ICWSM14/paper/view/8109

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# here replace this with your setup for the sentiment analyzer
s = SentimentIntensityAnalyzer()

def get_sentiment(text):
    # here put your code for analyzing a single tweet called `text'
    return s.polarity_scores(text)['compound']

##
