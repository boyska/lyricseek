import urllib
import urllib2

import lxml.html

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

class LyricsMania(object):
    name = 'LyricsMania'
    features = ('lyrics',)

    @staticmethod
    def _search(song_metadata):
        search = "%(artist)s %(title)s" % song_metadata
        query = urllib.urlencode({'k': search, 'x':'0', 'y': '0'})
        url = 'http://www.lyricsmania.com/searchnew.php?%s' % query
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('#albums>h1>a')

#this sorting hell is just to find the better result: lyricsmania sucks at this
        search = "%(artist)s - %(title)s" % song_metadata
        relative = sorted(links, key=lambda x:
            levenshtein(x.text.lower(), search.lower()))[0].get('href')
        return 'http://www.lyricsmania.com' + relative

    @staticmethod
    def get_data(song_metadata, option):
        url = LyricsMania._search(song_metadata)
        lyr = LyricsMania._get_lyrics_from_url(url)
        return {'lyrics':lyr}

    @staticmethod
    def _get_lyrics_from_url(url):
        content = urllib2.urlopen(url)
        page = lxml.html.parse(content)
        div = page.getroot().get_element_by_id('songlyrics_h')
        return ''.join([text for text in div.itertext()])

if __name__ == '__main__':
    print LyricsMania.get_data({'artist':'erode', 'title':'tempo che non ritorna'}, {})
