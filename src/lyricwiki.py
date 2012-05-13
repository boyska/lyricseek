#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import urllib2
import re

#import eyeD3
#from eyeD3.tag import *

cache = dict()
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def usage():
    print "usage: %s <artist> <title>" % sys.argv[0]
    sys.exit(1)


def getWikiLyrics(artist, song):
    """
    Fetch lyrics from lyrics.wikia.org
    """
    MARKER_STARTLYRICS = '&lt;lyrics&gt;'
    MARKER_STOPLYRICS = '&lt;/lyrics&gt;'
    MARKER_NOLYRICS = 'PUT LYRICS HERE'
    # normalize the titiles for lwiki
    artist = artist.replace(' ', '_')
    song = song.replace(' ', '_')

    lyrics_re = ur"%s(.*)%s" % (MARKER_STARTLYRICS, MARKER_STOPLYRICS)
    pat = re.compile(lyrics_re, re.S | re.I | re.M)

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
    return lyrics


def fillTrackLyrics(artist, song):
    '''
    A simple interface for getWikiLyrics
    '''

    #artist = Rammstein
    #song = Du_Hast
    print "Getting lyrics from lyricwiki.org for '%s' - '%s'" % (artist, song)
    lyrics = None
    try:
        lyrics = getWikiLyrics(artist, song)
        #lyrics = lyrics.decode("utf-8")
    except:
        print "Error while opening: %s" % sys.exc_info()
        return None

    if lyrics:
        print "Lyrics found. Updating file...",
        print "----------------------"
        print lyrics
        print "----------------------"
        print "file updated."
    else:
        print "Lyrics are not found"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    else:
        fillTrackLyrics(sys.argv[1], sys.argv[2])
