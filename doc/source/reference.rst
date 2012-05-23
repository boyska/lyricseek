API Reference
=============

User API
--------

User API is just one function, nothing more to worry about!

The typical usage is::

    import lyricseek
    lyricseek.get(artist='The Beatles', title='Let it be', request=('lyrics',))

.. autofunction :: lyricseek.get

Developer API
-------------

This modules are meant to be used for internal developers, or for the user who
know what he is doing.

_run
~~~~~~~~~~

.. automodule :: lyricseek._run
  :members:

pluginsystem
~~~~~~~~~~~~

.. automodule :: lyricseek._pluginsystem
  :members:
