#download Hypem playlists

import requests
import json
from bs4 import BeautifulSoup

HYPE_URL = 'http://www.hypem.com/'
user = 'kenanM'

def tracks(user):
    # Iterates through every track in a HypeMachine users account
    url = 'http://www.hypem.com/%s' % user
    while True:
        response = requests.get(url)
        doc = BeautifulSoup(response.content)
        data = doc.find(id='displayList-data')
        contents = json.loads(data.contents[0])
        for track in contents['tracks']:
            yield track
        if 'page_next' in contents:
            url = 'http://www.hypem.com%s' % contents['page_next']
        else:
            break

for track in tracks(user):
    print track
    #get the mp3 url
    #download the mp3
