import urllib
import urllib2

import lxml.html


class SongLyrics(object):
    name = 'SongLyrics'
    features = ('lyrics',)

    @staticmethod
    def _search(song_metadata):
        search = "%(artist)s %(title)s" % song_metadata
        artist = song_metadata['artist'].lower()
        title = song_metadata['title'].lower()
        search = "%s %s" % (artist, title)
        search = search.replace(' ', '+')
        url = 'http://www.songlyrics.com/index.php?section=search&searchW=%s&submit=Search' % search
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('div.serpdesc-2>a')
        links=links[0].get('href')
        return links


    @staticmethod
    def get_data(song_metadata, option):
        url = SongLyrics._search(song_metadata)
        lyr = SongLyrics._get_lyrics_from_url(url)
        return {'lyrics':lyr}

    @staticmethod
    def _get_lyrics_from_url(url):
        content = urllib2.urlopen(url)
        page = lxml.html.parse(content)
        div = page.getroot().get_element_by_id('songLyricsDiv')
        text = ''.join([text for text in div.itertext()])
        return text

if __name__ == '__main__':
    print SongLyrics.get_data({'artist':'michael jackson', 'title':'beat it'}, {})
