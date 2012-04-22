class MyRetriever(object):
    name = 'My Retriever'
    features = ('lyrics', 'coverart')  # choose a subset of this

    @staticmethod
    def get_data(song_metadata, option):
        # Edit me!!
        raise NotImplementedError()

if __name__ == '__main__':
    import types
    import sys

    retr = [cls for name, cls in  locals().items() if
            type(cls) is types.TypeType and name.endswith('Retriever')][0]
    artist = sys.argv[1]
    song = sys.argv[2]
    retr.get_data({'title': song, 'artist': artist}, {})
