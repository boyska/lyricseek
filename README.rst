What is lyricseek?
==================

LyricSeek is a do-it-all extendable, parallelized lyrics/coverart/metadata
fetching library; its main goal is to offer a reasonable alternative to
reinventing the wheel

**Do-it-all**: Not just lyrics!

**parallelized**: will support both thread-based and process-based parallelism
(todo)

**extendable**: lyricseek is a collection of "plugins" (called retrievers)
implemented through the egg system. It's easy to manage retrievers without
touching the library, and your package can provide a retriever, too.

Documentation
=============

Main documentation is available in doc/ directory.
You just need to execute ``make clean coverage html`` and you'll nice
documentation in ``build/html/index.html``

Install
=======

Package installation should be provided through a setup.py script, but it still
is a TODO.

Develop How-to
==============

Files
-----

Directory structure::

  .
  |-- doc                       Documentation dir
  |   |-- build                 make-d files are here
  |   `-- source                Actual documentation files
  |-- retrievers                Some retrievers shipped with the library; see its README.txt
  `-- src                       The actual library
	  `-- plugin_skeleton       Plugin skeleton is what you should start with if writing a new retriever

Write a retriever
-----------------

See the Plugin Howto in the documentation
