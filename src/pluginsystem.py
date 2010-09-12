'''
This module provides access to plugins, metadata and other tools
'''
import pkg_resources

plugins = {}  # name:class


def load_plugins():
    '''
    Searches for plugins, and load them into memory.

    .. todo :: support plugin versions
    '''
    for entrypoint in pkg_resources.iter_entry_points('lyricseek.retriever'):
        if entrypoint.name in plugins:
            print 'WARNING: conflicting version of plugin "%s"' % \
                    entrypoint.name
            continue
        plugin = entrypoint.load()
        #do some checks
        if not hasattr(plugin, 'features') or not plugin.features or\
                not hasattr(plugin, 'get_data') or not hasattr(plugin, 'name'):
            print 'WARNING: plugin "%s" doesn\'t comply to the interface.'\
                    ' Not loading it'
            continue
        plugins[entrypoint.name] = plugin


def get_plugins():
    '''
    :returns: name:class dict of plugins (if loaded)
    '''
    return plugins


def get_plugin_features(name):
    '''
    :returns: supported features (see :ref:`retrievers`)
    :rtype: tuple of strings
    '''
    if not name in plugins:
        raise ValueError
    return plugins[name].features
