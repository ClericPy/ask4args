from typing import List, Dict


def test1(a: int,
          b: int = 4,
          *args_list: List[str],
          **args_dict: Dict[str, str]):
    print(vars())


def test2(a: int,
          b: int = 4,
          c: int = 5,
          *,
          loop: bool = False,
          loop2: str = 'st',
          **args_dict: Dict[str, str]) -> Dict[str, list]:
    """[summary]

    :param a: [description]
    :type a: int
    :param b: [description], defaults to 4
    :type b: int, optional
    :param c: [description], defaults to 5
    :type c: int, optional
    :param loop: [description], defaults to 33
    :type loop: int, optional
    :param loop2: [description], defaults to 'st'
    :type loop2: str, optional
    :return: [description]
    :rtype: Dict[str, list]
    """
    print(vars())


from ask4args.core import BaseSchema

ss = BaseSchema(test2)
# print(ss.arg_docs)
# print(ss.schema_args)
ss.run()
