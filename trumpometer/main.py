"""
This file does the core work of the project.
It should be left running on an uninterrupted computer, where it periodically reads the tweet file database and updates the output file accordingly.
"""
from sentiment import get_sentiment
from locations import get_location
from csv_parsing import read_last_nrows, dump_data
from tw_stream import KeywordListener
import time, threading

# Parameters
interval = 3 # seconds
n_most_recent = 100

# Runtime vars
t0 = time.clock()
lock = threading.Lock()
    
listener = KeywordListener(filename='data/raw_tweet_stream.csv', keywords=['trump'], rule='and', lock=lock)
listener.begin()

# Main loop
while True:
    if time.clock() - t0 < interval:
        continue

    #print('Next iteration.')

    # read in tweets
    tweets = read_last_nrows('data/raw_tweet_stream.csv', n_most_recent, lock=lock)
    if tweets is None:
        continue
    # extract important parameters
    sents = [get_sentiment(i) for i in tweets.text.values]
    locs = [get_location(i) for _,i in tweets.iterrows()]
    # format data
    data = pd.DataFrame(columns=['sentiment','state'])
    data.loc[:,'sentiment'] = sents
    data.loc[:,'state'] = locs
    mean_by_state = data.groupby('state').sentiment.mean()
    # dump data to file that web interface will read
    dump_data(mean_by_state)

    t0 = time.clock()

listener.end()
