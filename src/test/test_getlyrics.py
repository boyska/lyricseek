import time
import sys

from nose.tools import timed, raises

sys.path.append('..')
import get_lyrics
import pluginsystem

### Some dummy retrievers to test things


class Slow:
    name = 'slow'
    features = ('foo',)

    @staticmethod
    def get_data(*args, **kwargs):
        time.sleep(3)
        print 'slow ended'
        return {'foo': 'slow foo'}


class Quick:
    name = 'quick'
    features = ('foo',)

    @staticmethod
    def get_data(*args, **kwargs):
        print 'quick ended'
        return{'foo': 'quick foo'}


class Error:
    name = 'error'
    features = ('foo',)

    @staticmethod
    def get_data(*args, **kwargs):
        raise Exception("I'm the errorgiver. hello")


### test_generators (nose is cool)
def every_parallel(func):
    '''Run the test both with process-based and thread-based parallelism'''
    def gen(self):
        get_lyrics.set_parallel('process')
        yield func, self
        get_lyrics.set_parallel('thread')
        yield func, self
    gen.__name__ = func.__name__
    return gen


class TestParallelism:
    @raises(ValueError)
    def test_invalid_method(self):
        '''errors when invalid method'''
        get_lyrics.set_parallel('fooza')

    def test_good_methods(self):
        get_lyrics.set_parallel('process')
        get_lyrics.set_parallel('thread')

    #TODO: how to check if it is really thread based when choosing threads?


class TestGetLyrics:
    @every_parallel
    @timed(.5)
    def test_first_match(self):
        'first match analyzer should choose the quickest, and do it quick'
        #TODO: change to a more explicit, analyzer-choosing API
        pluginsystem.register_plugin('quick', Quick)
        pluginsystem.register_plugin('slow', Slow)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo',),
                analyzer='first_match')
        assert res[0] == 'quick'

    @every_parallel
    def test_first_dont_match(self):
        'first match should not match results that do not satisfies request'
        pluginsystem.register_plugin('quick', Quick)
        res = get_lyrics.get_lyrics('a', 'b', request=('donthaveit'),
                analyzer='first_match')
        assert res[0] == None

    @every_parallel
    def test_slow_if_no_matches(self):
        "when no matches are found, slowness is ok"
        pluginsystem.register_plugin('slow', Slow)
        pluginsystem.register_plugin('quick', Quick)
        start = time.time()
        res = get_lyrics.get_lyrics('a', 'b', request=('donthaveit'),
                analyzer='first_match')
        assert time.time() - start > 1.0

    @every_parallel
    def test_timeout(self):
        "Timeout must do its job"
        pluginsystem.register_plugin('slow', Slow)
        pluginsystem.register_plugin('quick', Quick)
        start = time.time()
        res = get_lyrics.get_lyrics('a', 'b', request=('donthaveit'),
                timeout=1)
        assert time.time() - start < 2.0

    @raises(ValueError)
    def test_bad_analyzer(self):
        get_lyrics.get_lyrics('a', 'b', analyzer='dontexist')

    def test_error_handling(self):
        '''Even when retrievers raise, all is fine'''
        pluginsystem.register_plugin('error', Error)
        get_lyrics.get_lyrics('a', 'b')
