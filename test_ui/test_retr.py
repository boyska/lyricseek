class Foo:
    name = 'Foo'
    features = ('lyrics',)

    @staticmethod
    def get_data(*args, **kwargs):
        return {'lyrics': 'asd'}
