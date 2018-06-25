import pytest

from tohsaka.qualifiers.qualifier import Qualifier

class TestQualifier:

    BASE_CONFIG = {
        'qualify': {
            'field': ['field'],
            'condition': {
                'type': '>',
                'value': 3
            }
        }
    }

    BASE_ITEM = {
        'field': 5,
        'wrong': {
            'test': 10
        }
    }

    def test_qualify_basic(self):
        qualifier = Qualifier(self.BASE_CONFIG)

        result = qualifier.go(self.BASE_ITEM)

        assert result


    def test_qualify_no_config(self):
        qualifier = Qualifier({})

        result = qualifier.go(self.BASE_ITEM)

        assert result

    def test_wrong_type(self):
        qualifier = Qualifier(self.BASE_CONFIG)

        item = self.BASE_ITEM
        item['field'] = {}

        result = qualifier.go(item)

        assert not result

    def test_qualify_greater_failed(self):
        qualifier = Qualifier(self.BASE_CONFIG)

        item = self.BASE_ITEM
        item['field'] = 1

        result = qualifier.go(item)

        assert not result

    def test_not_implemented(self):
        config = self.BASE_CONFIG
        config['qualify']['condition']['type'] = '<'
        qualifier = Qualifier(self.BASE_CONFIG)


        with pytest.raises(Exception):
            result = qualifier.go(self.BASE_ITEM)
