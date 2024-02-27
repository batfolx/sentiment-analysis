import os
import json
from benzinga import news_data
from typing import List

benzinga_api_key = os.getenv('BENZINGA_API_KEY')
if not benzinga_api_key:
    raise EnvironmentError("No BENZINGA_API_KEY found in the environment variables.")

paper = news_data.News(api_token=benzinga_api_key)
stories: List[dict] = paper.news()
with open('samples/sample-paper-news-output.json', 'w+') as f:
    json.dump(stories, f)
