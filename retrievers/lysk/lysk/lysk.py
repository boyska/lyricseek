import re
import urllib2

class lysk(object):
    name = 'lysk'
    features = ('lyrics', )

    @staticmethod
    def get_data(song_metadata, option):
        MARKER_STARTLYRICS = '&lt;lyrics>'
        MARKER_STOPLYRICS = '&lt;/lyrics>'
        MARKER_NOLYRICS = 'PUT LYRICS HERE'
        # normalize the titiles for lwiki
        artist = song_metadata['artist'].lower
        song = song_metadata['title'].lower
        artist = artist.replace(' ', '_')
        song = song.replace(' ', '_')

        lyrics_re = ur"%s(.*)%s" % (MARKER_STARTLYRICS, MARKER_STOPLYRICS)
        pat = re.compile(lyrics_re, re.S|re.I|re.M)

        lyrics = ""
        _url = "http://lyrics.wikia.com/index.php?title=%s:%s&action=edit" % \
                (artist, song)

        page = urllib2.urlopen(_url).read()
        if not page:
            raise Exception('Errors occured; nothing found')
        result = pat.findall(page)
        if result:
            lyrics = result[0]
        else:
            raise Exception('Errors while parsing')
        if lyrics.find(MARKER_NOLYRICS) > -1:
            lyrics = ""
        return {'lyrics':lyrics}

if __name__ == '__main__':
    import sys
    artist = sys.argv[1]
    song = sys.argv[2]
    retr.get_data({'title':song, 'artist': artist}, {})
