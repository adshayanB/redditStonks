from psaw import PushshiftAPI
import datetime
import finnhub
import pprint

api = PushshiftAPI()
dt = datetime.datetime.today()
date = int(datetime.datetime(dt.year,dt.month,dt.day).timestamp())
#Need to do env when we move it to backend 
finnhub_client = finnhub.Client(api_key="c371jnaad3ib6g7egdag")


articles = list(api.search_submissions(after = date,subreddit = 'wallstreetbets', filter =['url','author', 'title', 'subreddit'] ))
redditTickers ={}
for article in articles:
    words = article.title.split()
    tickers= list(filter(lambda word:word.lower().startswith('$'), words))

    if len(tickers)>0:
        for ticker in tickers:
            if(ticker.upper()[1:5] not in redditTickers):
                redditTickers[ticker.upper()[1:5]] = 1
            else:
                redditTickers[ticker.upper()[1:5]]+=1

redditTicker= {}
for key, value in redditTickers.items():
    if key.isalpha():
        redditTicker[key]=value

stockTickers = dict(sorted(redditTicker.items(), key=lambda x: x[1],reverse=True))
stockVal = {}
for key in stockTickers.items():
    value = finnhub_client.quote(key)
    if (value['t'] !=0):
        stockVal[key] = value
        
#Formats dictionary in a nice easy to read form
pprint.pprint(stockVal)