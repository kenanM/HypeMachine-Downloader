#download Hypem playlists

from bs4 import BeautifulSoup
import requests
import json
import os
import string

HYPE_URL = 'http://www.hypem.com/'
ALLOWED_CHARACTERS = '-_.() %s%s' % (string.ascii_letters, string.digits)


user = 'kenanM'
DOWNLOAD_FOLDER = '/home/kenan/Media/Music'

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

def clean_file_name(string):
    return ''.join(c for c in string if c in ALLOWED_CHARACTERS)

def generate_file_name(track):
    artist = track['artist'].encode('ascii', 'ignore')
    song = track['song'].encode('ascii', 'ignore')
    return '%s - %s.mp3' % (artist, song)

def get_mp3_link(track):
    pass

for track in tracks(user):
    if track['type'] is False:
        print 'Skipping %s as it is no longer available' % file_name
        continue

    file_name = generate_file_name(track)
    if file_name in os.listdir(DOWNLOAD_FOLDER):
        print 'Skipping %s as it has already been downloaded' % file_name
        continue

    mp3_link = get_mp3_link(track)

    #download the mp3
