import requests
import pandas as pd
from datetime import datetime as dt

df = pd.read_json("posts.json")
user_list = df["author"].unique()
karma_info_list = {}

def get_reddit(url):
    try:
        base_url = url
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
        return request.json()
    except:
        print('An Error Occured')

for user in user_list:
    url = f"http://www.reddit.com/user/{user}/about.json"

    user_dict = get_reddit(url)
    name = user_dict.get("data", {}).get("name", 0)
    subscribers = user_dict.get("data", {}).get("subreddit", {}).get("subscribers", 0)
    karma = user_dict.get("data", {}).get("total_karma", {})
    if name:
        karma_info_list["name"] = [karma, subscribers]

df_users = pd.DataFrame(karma_info_list)

post_data = df_users.to_json("users.json")
print(karma_info_list)
