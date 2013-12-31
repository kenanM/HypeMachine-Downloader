#download Hypem playlists

from bs4 import BeautifulSoup
import requests
import json
import os
import string

ALLOWED_CHARACTERS = '-_() %s%s' % (string.ascii_letters, string.digits)

user = 'kenanM'
DOWNLOAD_FOLDER = '/home/kenan/Media/Music/hypem/'

class HypeDownloader:

    def init(self, user, download_folder):
        self.user = user
        self.download_folder = download_folder

    def _tracks(self, user, page_limit=1):
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

    def _clean_file_name(self, string):
        string = string.encode('ascii', 'ignore')
        return ''.join(c for c in string if c in ALLOWED_CHARACTERS)

    def _generate_file_name(self, track):
        artist = track['artist']
        song = track['song']
        file_name = '%s - %s' % (artist, song)
        return '%s.mp3' % self._clean_file_name(file_name)

    def _get_mp3_link(self, track):
        url = "http://hypem.com/serve/source/%s/%s" % (track['id'], track['key'])
        response = requests.get(url, cookies=track['cookie']).json()
        return response['url']

    def _download_mp3(self, url, download_location):
        response = requests.get(url)
        with open(download_location, "wb") as _file:
            for chunk in response.iter_content(128):
                if not chunk:
                    break
                _file.write(chunk)

    def run(self, page_limit):
        for track in self._tracks(user, 1000):
            if track['type'] is False:
                print 'Skipping %s as it is no longer available' % file_name
                continue

            file_name = self._generate_file_name(track)
            if file_name in os.listdir(DOWNLOAD_FOLDER):
                print 'Skipping %s as it has already been downloaded' % file_name
                continue

            mp3_link = self._get_mp3_link(track)
            print 'Downloading %s' % file_name
            self._download_mp3(mp3_link, '%s/%s' % (DOWNLOAD_FOLDER, file_name))

if __name__ == "__main__":
    HypeDownloader(user, download_folder).run(page_limit)