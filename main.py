from datetime import datetime as dt
import requests
import pandas as pd


subreddit = 'SnapLenses'
limit = 100
timeframe = None #'all'  # hour, day, week, month, year, all
listing = 'new'  # controversial, best, hot, new, random, rising, top
before = None
after = None
created = 1619820000 #start 2020
result_date = dt.now().timestamp()

def get_reddit(subreddit, listing, limit, timeframe, before):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}&before={before}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


to_extract = ['name','score', 'created','num_comments','view_count','ups',
              'downs', 'author', 'title','send_replies', 'view_count', 'category',
              'is_video','url','selftext']

posts_list = []

while created < result_date :

    response = get_reddit(subreddit, listing, limit, timeframe, before)["data"]["children"]
    
    for post in response:
            posts_list.append({e: post["data"][e] for e in to_extract })
    
    if len(response):

        before = response[-1]["data"]["name"]
        result_date = response[-1]["data"]["created"]
        print(f'{before} next set')

    else:
        break

df = pd.DataFrame(posts_list)

post_data = df.to_json("posts.json")
