from nose.tools import assert_false, raises

import pluginsystem


class TestCheck:
    def missing_features_test(self):
        class Missing:
            name = 'foo'

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(Missing))

    def missing_name_test(self):
        class Missing:
            features = ('foo')

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(Missing))

    def missing_getdata_test(self):
        class Missing:
            name = 'foo'
            features = ('foo',)
        assert_false(pluginsystem._check_plugin(Missing))

    def empty_features_test(self):
        class NoFeatures:
            name = 'foo'
            features = ()

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(NoFeatures))

    def empty_name_test(self):
        class NoName:
            name = ''
            features = ('foo',)

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(NoName))

    def features_wrong_type_test(self):
        class NoName:
            name = 'foo'
            features = ('foo')  # this is NOT a tuple!

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(NoName))

    def name_wrong_type_test(self):
        class NoName:
            name = ['foo']  #this is not a string
            features = ('foo',)

            def get_data(self):
                pass
        assert_false(pluginsystem._check_plugin(NoName))


class TestRegister:
    @raises(ValueError)
    def nonvalid_raises_test(self):
        class Missing:
            name = 'foo'
            features = ('foo',)
        pluginsystem.register_plugin('fooname', Missing)

