import sys
import os.path

import lyricseek

def overload_plugins(filepath, classname):
    filedir = os.path.dirname(filepath)
    filename = os.path.basename(filepath).split('.', 2)[0]
    sys.path = [filedir] + sys.path
    mod = __import__(filename, globals(), locals(), [classname], -1 )
    cls = getattr(mod, classname)
    lyricseek._pluginsystem.register_plugin(cls)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: %s /path/to/retriever.py ClassName title' % (sys.argv[0],)
        sys.exit(255)

    overload_plugins(sys.argv[1], sys.argv[2])
    print lyricseek.get(title=sys.argv[4], artist=sys.argv[3],
            request=('lyrics',))

