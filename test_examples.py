from ask4args.core import Ask4Args, Ask4ArgsGUI, Ask4ArgsWeb
from typing import List, Dict


def test_normal_function(a: int, b: int = 2, **args_dict: Dict[str, int]):
    '''
    assert a == 1
    assert b == 2
    assert args_dict['c'] == 3
    '''
    assert a == 1
    assert b == 2
    assert args_dict['c'] == 3
    return ('success', vars())


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
    return ('success', vars())


class TestClass(object):

    def test_method(self, a: str, b: int = 1):
        assert a == ''
        assert b == 1
        return ('success', vars())

    @classmethod
    def test_class_method(cls, a: str, b: int = 1):
        assert a == ''
        assert b == 1
        return ('success', vars())


def test_defaults(a: int):
    assert a == 1
    return ('success', vars())


if __name__ == "__main__":
    # cls = Ask4ArgsWeb
    # cls = Ask4Args
    cls = Ask4ArgsGUI
    # =====================
    # =====================
    # ('success', {'a': 1, 'b': 2, 'args_dict': {'c': 3}})
    cls(test_normal_function).run()
    # =====================
    # ('success', {'a': 1.1, 'b': 2, 'c': False, 'd': 'string', 'e': 1, 'f': [1, 2, 3], 'args_dict': {'h': 3}})
    cls(test_keyword_only_function,
        choices={
            'e': [1, 2, 3, 4, 5]
        },
        checkboxes={
            'f': [1, 2, 3, 4, 5]
        }).run()
    # =====================
    cls(TestClass().test_method).run()
    # =====================
    cls(TestClass().test_class_method).run()
    # =====================
    cls(test_defaults, defaults={'a': 1}).run()
    pass
