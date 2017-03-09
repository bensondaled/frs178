import tweepy as tw
import csv, time

api_key = '5ASetgbBUfjPLTx4lIRNB7wr1'
api_secret = '2dw02uFT3weZELbEiF9MiRAPL1K3MXK3i7vaQAkerqGVZC2Ejn'
access_token = '96322197-ckWyFTrUhC1quJLiV6bKlCkbVdv0HmUF7ZILJHSNz'
access_token_secret = 'X4BShDBALQLmbsyshnS7V5RZGM0oxK6dCajOjTbPXdKfc'

auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

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

    def __init__(self, api, filename, keywords=[], rule='or'):
        super(KeywordListener, self).__init__()

        # open a file to save tweets
        self.f = open(filename, 'a')
        self.writer = csv.DictWriter(self.f, fieldnames=['timestamp', 'text', 'user', 'loc'])
        self.writer.writeheader()
        self.f.flush()

        # set keywords of interest
        self.keywords = keywords

        # set the rule: AND or OR
        self.rule = rule

        self.stream = tw.Stream(auth = api.auth, listener=self)

    def begin(self):
        self.stream.filter(track=self.keywords, async=True)

    def on_status(self, status):
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

        self.writer.writerow(tweet_dict)
        self.f.flush()

    def on_error(self, code):
        print('Error {}'.format(code))

    def end(self):
        self.stream.disconnect()

if __name__ == '__main__':
    listener = KeywordListener(api=api, filename='mytweets.csv', keywords=['trump'], rule='and')
    listener.begin()

    #listener.end()
