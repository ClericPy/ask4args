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
                               e: int = None,
                               f: List[int] = None,
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
    assert a == 1.1
    assert b == 2
    assert c is False
    assert d == 'string'
    assert e == 1
    assert f == [1, 2, 3]
    assert args_dict['h'] == 3
    return args_dict


class TestClass(object):

    def test_method(self, a: str, b: int = 1):
        assert a == ''
        assert b == 1

    @classmethod
    def test_class_method(cls, a: str, b: int = 1):
        assert a == ''
        assert b == 1


def test_defaults(a: int):
    assert a == 1


if __name__ == "__main__":
    # Ask4Args(test_normal_function).run()
    # Ask4Args(test_keyword_only_function,
    #          choices={
    #              'e': [1, 2, 3, 4, 5]
    #          },
    #          checkboxes={
    #              'f': [1, 2, 3, 4, 5]
    #          }).run()
    # Ask4Args(TestClass().test_method).run()
    # Ask4Args(TestClass().test_class_method).run()
    # Ask4Args(test_defaults, defaults={'a': 1}).run()
    pass
