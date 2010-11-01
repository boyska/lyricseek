from distutils.core import setup

setup(name='LyricSeek',
      version='0.1',
      description='Lyrics and other metadata retrieving',
      long_description=open('README.rst', 'r').read(),
      author='Davide Lo Re',
      author_email='piuttosto@logorroici.org',
      packages=['lyricseek'],
      package_dir={'lyricseek': 'src'}
     )

