## Authenticate the API
import tweepy as tw

api_key = '5ASetgbBUfjPLTx4lIRNB7wr1'
api_secret = '2dw02uFT3weZELbEiF9MiRAPL1K3MXK3i7vaQAkerqGVZC2Ejn'
access_token = '96322197-ckWyFTrUhC1quJLiV6bKlCkbVdv0HmUF7ZILJHSNz'
access_token_secret = 'X4BShDBALQLmbsyshnS7V5RZGM0oxK6dCajOjTbPXdKfc'

auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

## Select your user of interest, called "root"
# (in practice, this would be the author of a randomly sampled tweet)
# (but for now, I'll use just one account as an example)

root = 'washingtonpost'

## collect ids of the all the friends of root
# limit is 5000 per call (which comes as pages using cursor api)
# I think you have 15 of these in 15 mins -> 75,000 friends
# https://dev.twitter.com/rest/reference/get/friends/ids
ids = [fr for fr in 
            tw.Cursor(api.friends_ids, screen_name=root, count=5000).pages()]

# * now you do that repeatedly and store thousands of IDs
# then run the "most-common" determination on this list of IDs, before moving on

## once you have a bunch of ids, from many users, find the associated screennames
# limit is 100 per call (no cursor needed here)
# I think you have 180 of these in 15 mins -> 18,000 id-to-name conversions
# you should only need to call this 10 times for your goal of 1000 most common, because those computations happened at the level of user ID
# https://dev.twitter.com/rest/reference/get/users/lookup
batch_size = 100
n_batches = int(np.ceil(len(ids)/batch_size))
users = [api.lookup_users(ids[i*batch_size:i*batch_size+batch_size]) 
            for i in range(n_batches)]
# flatten the list:
users = [u for ul in users for u in ul]

screen_names = [u.screen_name for u in users]

##

