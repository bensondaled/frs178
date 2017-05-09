##
# vader: http://www.aaai.org/ocs/index.php/ICWSM/ICWSM14/paper/view/8109

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

s = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return s.polarity_scores(text)['compound']

##
