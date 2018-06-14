from tohsaka.qualifiers.qualifier import Qualifier

class TestQualifier:

    BASE_CONFIG = {
        "qualify": {
            "field": ["field"],
            "condition": {
                "type": ">",
                "value": 3
            }
        }
    }

    BASE_ITEM = {
        "field": 5,
        "wrong": {
            "test": 10
        }
    }

    def test_qualify_basic(self):
        qualifier = Qualifier(self.BASE_CONFIG)

        qualifier.go(self.BASE_ITEM)