#download Hypem playlists

import requests
import json
from bs4 import BeautifulSoup

HYPE_URL = 'http://www.hypem.com/'
user = 'kenanM'

def tracks(user, page_limit=1):
    # Iterates through every track in a HypeMachine users account
    url = 'http://www.hypem.com/%s' % user
    while True:
        response = requests.get(url)
        data = BeautifulSoup(response.content).find(id='displayList-data')
        data = json.loads(data.contents[0])
        for track in data['tracks']:
            yield track
        if 'page_next' in data and data['page_num'] < page_limit:
            url = 'http://www.hypem.com%s' % data['page_next']
        else:
            break

for track in tracks(user):
    print track
    #get the mp3 url
    #download the mp3
