import os
import sys
import types

from setuptools import setup, find_packages


def autodetect():
    dirs = find_packages()
    if not dirs:
        print 'ERROR! No found packages!'
        sys.exit(1)
    if len(dirs) > 1:
        print 'ERROR! This retriever is non-standard' \
                ' (more than one directory found)'
        sys.exit(1)
    py_files = [f for f in os.listdir(dirs[0]) if f.endswith('.py') and
            not f.startswith('.') and not f.startswith('_')]
    if len(py_files) == 1:
        retriever_file = py_files[0]
    else:
        #euristics here
        retr_files = [f for f in py_files if f.find('retriever') != -1]
        if len(retr_files) == 1:
            retriever_file = retr_files[0]
        else:
            print "ERROR! Can't detect retriever file (too many files)"
            sys.exit(1)
    retr = getattr(__import__(dirs[0], fromlist=(retriever_file[:-3],)),
            retriever_file[:-3])
    exposed = [obj for obj in dir(retr) \
            if not obj.startswith('_') and\
            type(getattr(retr, obj)) is types.TypeType]
    if len(exposed) == 1:
        retr_class = getattr(retr, exposed[0])
    else:
        print "ERROR! Can't detect retriever file (too many exposed objects)"
        print exposed
        sys.exit(1)
    return {'name': retr_class.name, 'class_name': retr_class.__name__,
            'dir': dirs[0], 'file': retriever_file[:-3]}

detected = autodetect()
setup(
    name=detected['class_name'],  # TODO: autodetect
    version="0.1",  # TODO: autodetect
    packages=find_packages(),
    entry_points={
        # TODO: autodetect
        'lyricseek.retriever':\
                ['%(name)s = %(dir)s.%(file)s:%(class_name)s' % detected]})
