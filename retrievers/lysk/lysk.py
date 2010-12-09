class lysk(object):
    name = 'lysk'
    features = ('lyrics')

    @staticmethod
    def get_data(song_metadata, option):
        MARKER_STARTLYRICS = '&lt;lyrics&gt;'
        MARKER_STOPLYRICS = '&lt;/lyrics&gt;'
        MARKER_NOLYRICS = 'PUT LYRICS HERE'
        # normalize the titiles for lwiki
        artist = song_metadata['artist']
        song = song_metadata['title']
        artist = artist.replace(' ', '_')
        song = song.replace(' ', '_')

        lyrics_re = ur"%s(.*)%s" % (MARKER_STARTLYRICS, MARKER_STOPLYRICS)
        pat = re.compile(lyrics_re, re.S|re.I|re.M)

        lyrics = ""
        print artist
        print song
        _url = "http://lyrics.wikia.com/index.php?title=%s:%s&action=edit" % \
                (artist, song)

        page = urllib2.urlopen(_url).read()
        result = pat.findall(page)
        if result:
            lyrics = result[0]
        if lyrics.find(MARKER_NOLYRICS) > -1:
            lyrics = ""
        return {'lyrics':lyrics}

if __name__ == '__main__':
    import types
    import sys
    import urllib2
    import re


    retr = [cls for name, cls in  locals().items() if
            type(cls) is types.TypeType and name.endswith('Retriever')][0]
    artist = sys.argv[1]
    song = sys.argv[2]
    retr.get_data({'title':song, 'artist': artist}, {})
