import urllib
import urllib2

import lxml.html

class AlbumArtRetriever(object):
    name = 'albumart.org'
    features = ('coverart',)  # choose a subset of this

    @staticmethod
    def _search(song_metadata):
        search = "%(artist)s %(album)s" % song_metadata
        query = urllib.urlencode({'searchkey': search, 'itempage': '1',
            'newsearch':'1', 'searchindex':'Music'})
        url = 'http://www.albumart.org/index.php?%s' % query
        page = lxml.html.parse(urllib2.urlopen(url))
        return page
    @staticmethod
    def _extract(page):
        big_image = page.getroot().cssselect('#main_left a.thickbox')[0]
        return big_image.get('href')

    @staticmethod
    def get_data(song_metadata, option):
        # Edit me!!
        return {'coverart':
                AlbumArtRetriever._extract(AlbumArtRetriever._search(song_metadata)) }

if __name__ == '__main__':
    import types
    import sys

    retr = [cls for name, cls in  locals().items() if
            type(cls) is types.TypeType and name.endswith('Retriever')][0]
    artist = sys.argv[1]
    album = sys.argv[2]
    print retr.get_data({'artist': artist, 'album': album}, {})
