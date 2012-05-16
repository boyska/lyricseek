import urllib
import urllib2
import contextlib
import itertools

import lxml.html

class DepositoRetriever(object):
    name = 'ildeposito'
    features = ('lyrics',)  # choose a subset of this

    @staticmethod
    def _search(song_metadata):
        search = "%(title)s" % song_metadata
        query = urllib.urlencode({'ricerca': search, 'tipo':'canto',
            'tipologia': 'normale',
            'submit.x': '0', 'submit.y': '0'})
        url = 'http://www.ildeposito.org/ricerca.php?%s' % query
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('#contenuto a')

        links = [l.get('href') for l in links]
#some links refer to whole artists, or album.
#This ensure that only links to lyrics are chosen
        valid_links = itertools.ifilter(
                lambda l: l.startswith('http://www.ildeposito.org/archivio/canti/canto.php'),
                links)
        return valid_links.next()

    @staticmethod
    def _get_lyrics_from_url(url):
        with contextlib.closing(urllib2.urlopen(url)) as content:
            page = lxml.html.parse(content)

        div = page.getroot().cssselect('#virgola_dx')[0]
        return div.text

    @staticmethod
    def get_data(song_metadata, option):
        # Edit me!!
        url = DepositoRetriever._search(song_metadata)
        lyrics = DepositoRetriever._get_lyrics_from_url(url)
        return {'lyrics': lyrics}

if __name__ == '__main__':
    import types
    import sys

    retr = [cls for name, cls in  locals().items() if
            type(cls) is types.TypeType and name.endswith('Retriever')][0]
    artist = sys.argv[1]
    song = sys.argv[2]
    print retr.get_data({'title': song, 'artist': artist}, {})['lyrics']

# vim: set syntax=python:
