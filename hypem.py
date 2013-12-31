#download Hypem playlists

from bs4 import BeautifulSoup
import requests
import json
import os
import string

HYPE_URL = 'http://www.hypem.com/'
ALLOWED_CHARACTERS = '-_() %s%s' % (string.ascii_letters, string.digits)

user = 'kenanM'
DOWNLOAD_FOLDER = '/home/kenan/Media/Music/hypem/'

def tracks(user, page_limit=1):
    # Iterates through every track in a HypeMachine users account
    url = 'http://www.hypem.com/%s' % user
    while True:
        response = requests.get(url)
        data = BeautifulSoup(response.content).find(id='displayList-data')
        data = json.loads(data.contents[0])
        for track in data['tracks']:
            track['cookie'] = response.cookies
            yield track
        if 'page_next' in data or data['page_num'] < page_limit:
            url = 'http://www.hypem.com%s' % data['page_next']
        else:
            break

def clean_file_name(string):
    string = string.encode('ascii', 'ignore')
    return ''.join(c for c in string if c in ALLOWED_CHARACTERS)

def generate_file_name(track):
    artist = track['artist']
    song = track['song']
    file_name = '%s - %s' % (artist, song)
    return '%s.mp3' % clean_file_name(file_name)

def get_mp3_link(track):
    url = "http://hypem.com/serve/source/%s/%s" % (track['id'], track['key'])
    response = requests.get(url, cookies=track['cookie']).json()
    return response['url']

def download_mp3(url, download_location):
    response = requests.get(url)
    with open(download_location, "wb") as _file:
        for chunk in response.iter_content(1024):
            if not chunk:
                break
            _file.write(chunk)

for track in tracks(user, 1000):
    if track['type'] is False:
        print 'Skipping %s as it is no longer available' % file_name
        continue

    file_name = generate_file_name(track)
    if file_name in os.listdir(DOWNLOAD_FOLDER):
        print 'Skipping %s as it has already been downloaded' % file_name
        continue

    mp3_link = get_mp3_link(track)
    print 'Downloading %s' % file_name
    download_mp3(mp3_link, '%s/%s' % (DOWNLOAD_FOLDER, file_name))
