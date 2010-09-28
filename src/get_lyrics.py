'''
Main module: provide simple, ready-to-use functions
to get lyrics
'''
import functools

import pluginsystem


def get_ready_retrievers(artist=None, album=None, title=None, otherinfo=None, \
        request=(), timeout=-1, filename=None):
    '''
    .. note :: this is not meant to be used by the casual user. Use it if
      you are a developer or if you really do what you're doing

    This function will return an iterator over functions that take no arguments
    and will try to get data (that is, retrievers with arguments filled in)

    :param otherinfo: Other metadata, not worthing a function parameter
    :type otherinfo: dict
    :param request: all needed metadata. If empty, all will be searched
    :type request: tuple
    :param timeout: currently not supported
    :rtype: iterator
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

    for name, plugin in pluginsystem.get_plugins().items():
        yield name, functools.partial(plugin.get_data, song_metadata, options)
    return


def get_lyrics(artist=None, album=None, title=None, otherinfo=None, \
        request=(), timeout=-1, filename=None):
    '''
    .. todo :: use multiprocessing

    Simply get lyrics

    :param otherinfo: Other metadata, not worthing a function parameter
    :type otherinfo: dict
    :param request: all needed metadata. If empty, all will be searched
    :type request: tuple
    :param timeout: currently not supported
    :rtype: dict
    '''
    res = {}
    for name, retriever in get_ready_retrievers(artist, album, title, \
            otherinfo, request, timeout, filename):
        try:
            result = retriever()
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
