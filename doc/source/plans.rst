Plans for the library
=====================

.. note ::
  
  None of this has been implemented yet. See :doc:`status` for more
  informations

This is a sort of project of what the library should look like when finished.

* A decent name :)
* Low, if not none, dependencies
* There is a simple but powerful api

  * ``get_lyrics(artist='foo', album='asd', title='xyz', otherinfo='this', timeout=10)``
    Just do it.
  * ``get_lyrics_fastest(... as above ...)``
    The first site to give an 'OK' will return
  * .. todo :: ``get_lyrics_best(... as above ...)``

    Try to catch as much information as possible
  * .. todo :: ``get_lyrics_all(... as above ...)``

    Return all results (useful for user selection) *
  * .. todo :: ``get_lyrics(filename='/path/to/file.mp3, id3=True)`` 
    
    will automatically
    discover album, artist, title information using file metadata. This will
    work, however, only if eyed3 is installed

* It's not limited to lyrics, but supports artist info, cover, tabs, whatsoever
* Extensibility is provided through eggs

  * see http://base-art.net/Articles/64/ (only useful if you already know eggs)
  * plugin are separate packages
  * any package can contain entrypoint for our library
  * each plugin is called a Retriever

* .. todo :: Retrievers run concurrently, results analysis is performed real*time

  * This way we can take "the fastest", or wait for the best
  * An asyncronous API should be provided
	* This way a software can see the lyrics coming in real*time when he is
	  calling get_lyrics_all, not having to wait for all the lyrics to be fetched
	  (it is especially useful because there will probably some plugin behaving
	  badly, and we don't want it to ruin our work). 
	  And, yeah, there is timeout, but it's not a complete solution
  
  * .. seealso ::
        
        Section on :ref:`retrievers`

* .. todo :: A command*line utility provides the same functionalities 

  * Different outputs (human, colour, parseable)

* .. todo :: A C library that wraps the python one

.. _retrievers:

Retrievers
----------

.. highlight:: python

A retriever is an object that can fetch lyrics, coverart or other stuff.
It is a class with a lot of metadata about his capabilities (optional),
and one mandatory static method, ``get_data``

No subclassing is required, only conventional class attributes are needed.

Let's see an example::

    class FooRetriever(object):
        name = 'Foo will do'
        features = ('lyrics', 'coverart')

        @staticmethod
        def get_data(song_metadata, options)

The more interesting part is ``get_data``: here all the fetching part is done.
Both his tho arguments, ``song_metadata`` and ``options`` are dict.
``song_metadata`` has four main fields: ``artist``, ``title``, ``album``,
``filename``. Some of them could be None.
``options`` has currently only one field, but it may grow:

* ``searching`` A tuple containing what the user wants (similar to features).
  It can be useful to reduce time: suppose, for example, that your function can
  fetch both lyrics and coverart, but is slow on the latter. If the user is
  only searching lyrics, there's no need to fetch coverart

To know how to create a retriever plugin, read :doc:`plugin_howto`

setup.py
~~~~~~~~
The ``setup.py`` you'll find into the plugin skeleton is slightly modified
to make it more "automatic": the entrypoint name is equal to ``Retriever.name``,
and attempts are done to autoconfigure it.
If you have a complex file structure, or defines other classes than the Retriver one, it will probably fail.
It should be easy, anyway, to configure it!
