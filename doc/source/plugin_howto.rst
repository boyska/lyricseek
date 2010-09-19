Plugin HOWTO
============

You will find a "plugin skeleton": it consists of a
``setup.py`` plus the "real" plugin directory.

The plugin is basicly a class with a lot of metadata and one (static)method.
You should just fill-in metadata and code your method as you prefer.

To use the plugin, we use the egg system: for you, this means that you have to
build a "distribution" (a .egg file) for your plugin.
You can do it with ``python setup.py bdist_egg``.
Then, anyone can install it using ``easy_install``.

Development mode
----------------
If you are developing the plugin, you'll probably find yourself continously
creating an egg and instaling it. This is boring!

It's probably easier to do ``sudo python setup.py develop``: this will create a
sort of link, so that you won't need to reinstall it.

Testing it easy
---------------
.. todo :: this has not been done

The skeleton should contain a basic command-line interface to test your plugin.
This will eliminate the need to use the library to test it.

Dependencies
------------
If your plugin has any dependencies, you should write this in ``setup.py``.
