"""
This file defines a class for constantly reading tweets and writing them to a csv.
It should be called from the main.py file
"""

import tweepy as tw
import csv, time

class KeywordListener(tw.StreamListener):
    """
    A class for reading and saving live tweets using the twitter streaming API through tweepy

    Parameters
    ----------
    api : tweepy API object
    generated using the appropriate keys and tokens
    filename : string 
    name of file into which to write tweets
    keywords : list
    list of keywords to filter for
    rule : 'or' / 'and'
    rule by which to filter which tweets are written to file

    To use: make an instance of the object. 
    Call begin() to start streaming, and end() to stop streaming. 
    Results will be saved into the specified file.
    """

    def __init__(self, filename, keywords=[], rule='or', lock=None):
        super(KeywordListener, self).__init__()
        
        api_key = '5ASetgbBUfjPLTx4lIRNB7wr1'
        api_secret = '2dw02uFT3weZELbEiF9MiRAPL1K3MXK3i7vaQAkerqGVZC2Ejn'
        access_token = '96322197-ckWyFTrUhC1quJLiV6bKlCkbVdv0HmUF7ZILJHSNz'
        access_token_secret = 'X4BShDBALQLmbsyshnS7V5RZGM0oxK6dCajOjTbPXdKfc'

        auth = tw.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth)

        # open a file to save tweets
        self.filename = filename
        self.f = open(filename, 'a')
        self.writer = csv.DictWriter(self.f, fieldnames=['timestamp', 'text', 'user', 'loc'])
        self.writer.writeheader()
        self.f.flush()
        self.f.close()

        self.lock = lock

        # set keywords of interest
        self.keywords = keywords

        # set the rule: AND or OR
        self.rule = rule

        self.stream = tw.Stream(auth = api.auth, listener=self)

        self.debug = 0

    def begin(self):
        self.stream.filter(track=self.keywords, async=True)

    def on_status(self, status):
        if self.debug==0:
            self.t = status
            self.debug = 1
        timestamp = time.time()
        text = status.text.lower()
        user = status.author.screen_name
        loc = status.user.location

        if self.rule == 'or':
            pass # this is by default
        elif self.rule == 'and':
            if not all([kw in text for kw in self.keywords]):
                return # skip the writing step if not all the keywords were present

        tweet_dict = dict(timestamp=timestamp, text=text, user=user, loc=loc)

        with self.lock, open(self.filename,'a') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'text', 'user', 'loc'])
            writer.writerow(tweet_dict)
            f.flush()

    def on_error(self, code):
        print('Error {}'.format(code))

    def end(self):
        self.stream.disconnect()

if __name__ == '__main__':
    listener = KeywordListener(api=api, filename='data/raw_tweet_stream.csv', keywords=['trump'], rule='and')
    listener.begin()

    #listener.end()
