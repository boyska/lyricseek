class MyRetriever(object):
    name = 'My Retriever'
    features = ('lyrics', 'coverart')  # choose a subset of this

    @staticmethod
    def get_data(song_metadata, option):
        # Edit me!!
        raise NotImplementedError()

def get_data():
    return 'asd'
