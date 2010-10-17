import time
import sys

from nose.tools import timed, raises
from nose.plugins.attrib import attr


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


class QuickBar:
    name = 'quick_bar'
    features = ('foo',)

    @staticmethod
    def get_data(*args, **kwargs):
        print 'quick_bar ended'
        return{'bar': 'quickBar bar'}


class Trackable:
    name = 'trackable'
    features = ('bar',)
    called = False

    @staticmethod
    def get_data(*args, **kwargs):
        Trackable.called = True
        return {'bar': 'tracked bar'}


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
    def setUp(self):
        #make sure that there are no registered plugins
        pluginsystem.plugins.clear()

    def tearDown(self):
        #make sure that there are no registered plugins
        pluginsystem.plugins.clear()

    @every_parallel
    @timed(.5)
    def test_first_match(self):
        'first match analyzer should choose the quickest, and do it quick'
        #TODO: change to a more explicit, analyzer-choosing API
        pluginsystem.register_plugin(Quick)
        pluginsystem.register_plugin(Slow)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo',),
                analyzer='first_match')
        assert res['foo'] == 'quick foo'

    def test_first_advanced_match(self):
        '''first match should "compose" results'''
        pluginsystem.register_plugin(Quick)
        pluginsystem.register_plugin(QuickBar)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo', 'bar'),
                analyzer='first_match')
        assert 'bar' in res
        assert 'foo' in res

    def test_first_dont_match(self):
        'first match should not match results that do not satisfies request'
        pluginsystem.register_plugin(Quick)
        res = get_lyrics.get_lyrics('a', 'b', request=('donthaveit'),
                analyzer='first_match')
        assert res == None

    @attr('slow')
    @every_parallel
    def test_slow_if_no_matches(self):
        "when no matches are found, slowness is ok"
        pluginsystem.register_plugin(Slow)
        start = time.time()
        res = get_lyrics.get_lyrics('a', 'b', request=('foo',),
                analyzer='first_match')
        assert time.time() - start > 1.0

    @attr('slow')
    @every_parallel
    def test_timeout(self):
        "Timeout must do its job"
        pluginsystem.register_plugin(Slow)
        pluginsystem.register_plugin(Quick)
        start = time.time()
        res = get_lyrics.get_lyrics('a', 'b', request=('donthaveit'),
                timeout=1)
        assert time.time() - start < 2.0

    @raises(ValueError)
    def test_bad_analyzer(self):
        get_lyrics.get_lyrics('a', 'b', analyzer='dontexist')

    def test_error_handling(self):
        '''Even when retrievers raise, all is fine'''
        pluginsystem.register_plugin(Error)
        get_lyrics.get_lyrics('a', 'b')

    @every_parallel
    def test_best_found(self):
        '''first_match must found the "best", even if not perfect'''
        pluginsystem.register_plugin(Slow)
        pluginsystem.register_plugin(QuickBar)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo', 'bar'),
                timeout=0.5)
        assert 'bar' in res
        assert 'foo' not in res

    @every_parallel
    def test_noone_is_fast_enough(self):
        '''when no retriever is fast enough, (None, None) should be returned'''
        pluginsystem.register_plugin(Slow)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo',),
                timeout=0.2)
        print 'NOONE', res
        assert res is None

    @attr('slow')
    def test_no_extra(self):
        '''Don't return anything that is not requested'''
        pluginsystem.register_plugin(Slow)
        pluginsystem.register_plugin(QuickBar)
        res = get_lyrics.get_lyrics('a', 'b', request=('foo',))
        print 'result', res
        assert 'foo' in res
        assert 'bar' not in res

    def test_useless_are_not_called(self):
        '''Retrievers which don't provide requested data are not called'''
        pluginsystem.register_plugin(Slow)
        pluginsystem.register_plugin(Trackable)
        get_lyrics.get_lyrics('a', 'b', request=('foo',), timeout=0.3)
        time.sleep(0.2)
        assert Trackable.called == False
