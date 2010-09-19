'''
Main module: provide simple, ready-to-use functions
to get lyrics
'''

import pluginsystem


def get_lyrics(artist=None, album=None, title=None, otherinfo=None, \
        request=(), timeout=-1, filename=None):
    '''
    Simply get_lyrics

    .. todo :: use multiprocessing
    :param otherinfo: Other metadata, not worthing a function parameter
    :type otherinfo: dict
    :param request: all needed metadata. If empty, all will be searched
    :type request: tuple
    :param timeout: currently not supported
    :returns: all the metadata found, as a type:value dict
    :rtype: dict
    '''
    song_metadata = otherinfo if otherinfo else {}
    if artist:
        song_metadata['artist'] = artist
    if album:
        song_metadata['album'] = album
    if title:
        song_metadata['title'] = title

    options = {}
    options['searching'] = request or ('lyrics', 'coverart')

    res = {}
    for name, plugin in pluginsystem.get_plugins().items():
        try:
            result = plugin.get_data(song_metadata, options)
        except:
            print 'WARNING! Plugin %s raised an exception' % name
        else:
            #TODO: add deeper checking
            if type(result) is dict:
                res[name] = result
            else:
                print 'WARNING! Plugin %s returned inconsistent output (%s)' %\
                        (name, result)
                print '\tIt probably is a plugin bug'

    first_res = {}
    for plugin, plugin_res in res.items():
        for key, value in plugin_res.items():
            if key not in first_res:
                first_res[key] = value

    return first_res
