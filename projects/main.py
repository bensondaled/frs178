from sentiment import get_sentiment

tweets = pd.read_csv('mytweets.csv')

states = pd.read_pickle('base_us_table.pd').code.values

locs = [i for i in tweets['loc'].values]
sents = [get_sentiment(i) for i in tweets.text.values]

result = []
for l,sent in zip(locs,sents):
    l = str(l)
    for s in states:
        s = str(s)
        if s in l:
            result.append((s,float(sent)))
            continue

data_ = pd.DataFrame(result, columns=['state','score'])
data_means = data_.groupby('state').score.mean()
