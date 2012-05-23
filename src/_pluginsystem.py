'''
This module provides access to plugins, metadata and other tools
'''
import types

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
        _check_plugin(plugin)
        plugins[entrypoint.name] = plugin


def _check_plugin(plugin):
    '''Perform some sanity checks'''
    if not hasattr(plugin, 'features') or not plugin.features or\
            not type(plugin.features) in (types.TupleType, types.ListType) or\
            not hasattr(plugin, 'get_data') or not hasattr(plugin, 'name')\
            or not plugin.name or not type(plugin.name) is str:
        print 'WARNING: plugin "%s" doesn\'t comply to the interface.'\
                ' Not loading it' % plugin
        return False
    return True


def register_plugin(plugin):
    '''
    .. warning :: This is only intended for debug or dirty h4x.
        If unsure, you shouldn't use this

    Register a plugin. Useful to add Retrievers without packing proper eggs

    :arg name: The name of the plugin. In the standard case, this is the name
      of the entrypoint
    :arg plugin: the Retriever class implementing your plugin (must implement
      the interface described in :ref:`retrievers`

    :raises ValueError: If the check on the plugin fails
    '''
    if not _check_plugin(plugin):
        raise ValueError("Plugin check failed")
    plugins[plugin.name] = plugin


def get_plugins():
    '''
    :returns: name:class dict of plugins (if loaded)
    '''
    if not plugins:
        load_plugins()
    return plugins
