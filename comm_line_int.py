#! /usr/bin/env python

import lyricseek
import sys


def CommandLineLS(song_metadata):


    try:
        song_metadata.update(lyricseek.get(
                artist=song_metadata['artist'], title=song_metadata['title'],
                request=('lyrics',)))
        print(song_metadata['lyrics'])
    except IOError:
        print "Errore nella ricerca dei testi"
        return 1
    return 0

if __name__ == '__main__':


    song_metadata = {'artist':sys.argv[1], 'title':sys.argv[2]}

    sys.exit(CommandLineLS(song_metadata))
