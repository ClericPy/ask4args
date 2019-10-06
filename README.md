# Ask4args
Terminal UI to generate config file without learning the documentary.


Inspired by [python-fire](https://github.com/google/python-fire), and it maybe need a human-friendly interactive UI.

https://pypi.org/project/ask4args/

> pip install ask4args -U

```python
from ask4args.core import Ask4Args
from typing import List, Dict


def test_normal_function(a: int, b: int = 2,
                         **args_dict: Dict[str, int]) -> str:
    # first a value=1, args_dict['c']=3, others use default.
    # press 1, enter, enter, enter, c, enter, 3, enter, enter
    assert a == 1
    assert b == 2
    assert args_dict['c'] == 3
    return 'success'


def test_keyword_only_function(a: float,
                               b: int = 2,
                               *,
                               c: bool = False,
                               d: str = 'string',
                               **args_dict: Dict[str, int]):
    """Read the doc, and test kw-only args.

    :param a: one float num
    :type a: float
    :param b: one int num, defaults to 4
    :type b: int, optional
    :param c: boolen arg, defaults to False
    :type c: bool, optional
    :param d: string arg, defaults to 'string'
    :type d: str, optional
    :return: return the args_dict
    :rtype: Dict[str, list]
    """
    # press y, 1.1, enter, enter, enter, enter, enter, e, enter, 3, enter, enter
    assert a == 1.1
    assert b == 2
    assert c is False
    assert d == 'string'
    assert args_dict['e'] == 3
    return args_dict


class TestClass(object):

    def test_method(self, a: str, b: int = 1):
        assert a == ''
        assert b == 1

    @classmethod
    def test_class_method(cls, a: str, b: int = 1):
        assert a == ''
        assert b == 1


def test_checkboxes(a: List[int]):
    assert a == [1, 2, 3]


def test_choices(a: int):
    assert a == 1


def test_defaults(a: int):
    assert a == 1


if __name__ == "__main__":
    # Ask4Args(test_normal_function).run()
    # Ask4Args(test_keyword_only_function).run()
    # Ask4Args(TestClass().test_method).run()
    # Ask4Args(TestClass().test_class_method).run()
    # Ask4Args(test_checkboxes, checkboxes={'a': [1, 2, 3, 4, 5]}).run()
    # Ask4Args(test_choices, choices={'a': [1, 2, 3, 4, 5]}).run()
    # Ask4Args(test_defaults, defaults={'a': 1}).run()
    pass




```
