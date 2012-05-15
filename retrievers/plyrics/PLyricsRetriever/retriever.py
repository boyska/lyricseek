import urllib
import urllib2
import contextlib

import lxml.html

class PLyricsRetriever(object):
    name = 'PLyrics'
    features = ('lyrics',)  # choose a subset of this

    @staticmethod
    def _search(song_metadata):
        search = "%(artist)s %(title)s" % song_metadata
        query = urllib.urlencode({'q': search, 'cs':'utf-8'})
        url = 'http://search.plyrics.com/search.php?%s' % query
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('.body a')

        links = [l.get('href') for l in links]
#some links refer to whole artists, or album.
#This ensure that only links to lyrics are chosen
        valid_links = [l for l in links if l.startswith('http://www.plyrics.com/lyrics/')]
        return valid_links[0]

    @staticmethod
    def _get_lyrics_from_url(url):
        with contextlib.closing(urllib2.urlopen(url)) as buf:
            content = buf.read()
#ugly, but no other solution worked fine
        content = content.split('<!-- start of lyrics -->',2)[1].\
                split('<!-- end of lyrics -->')[0]
        page = lxml.html.document_fromstring(content)
        return page.text_content()

    @staticmethod
    def get_data(song_metadata, option):
        url = PLyricsRetriever._search(song_metadata)
        lyrics = PLyricsRetriever._get_lyrics_from_url(url)
        return {'lyrics': lyrics}

if __name__ == '__main__':
    import types
    import sys

    retr = [cls for name, cls in  locals().items() if
            type(cls) is types.TypeType and name.endswith('Retriever')][0]
    artist = sys.argv[1]
    song = sys.argv[2]
    print retr.get_data({'title': song, 'artist': artist}, {})['lyrics']
