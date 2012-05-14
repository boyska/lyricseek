import urllib
import urllib2

import lxml.html


class MetroLyrics(object):
    name = 'MetroLyrics'
    features = ('lyrics',)

    @staticmethod
    def _search(song_metadata):
        search = "%(artist)s %(title)s" % song_metadata
        artist = song_metadata['artist']
        artist = artist.replace(' ', '+')
        title = song_metadata['title']
        title = title.replace(' ' , '+')
        search = "%s+%s" % (artist, title)
        urlroot = "http://www.metrolyrics.com"
        url = 'http://www.metrolyrics.com/search.php?category=ArtistTitle&search=%s' % search
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('#search-results>li>a')
        links=links[0].get('href')
        result = "%s%s" % (urlroot, links)
        return result


    @staticmethod
    def get_data(song_metadata, option):
        url = MetroLyrics._search(song_metadata)
        lyr = MetroLyrics._get_lyrics_from_url(url)
        return {'lyrics':lyr}

    @staticmethod
    def _get_lyrics_from_url(url):
        content = urllib2.urlopen(url)
        page = lxml.html.parse(content)
        div = page.getroot().get_element_by_id('lyrics-body')
        text = ''.join([text for text in div.itertext()])
        return text

if __name__ == '__main__':
    print MetroLyrics.get_data({'artist':'coldplay', 'title':'paradise'}, {})
