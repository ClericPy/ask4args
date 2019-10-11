import inspect
from copy import deepcopy
from functools import partial
from inspect import Parameter
from pathlib import Path
from typing import Any, AnyStr, Dict, List, _alias, _GenericAlias, _SpecialForm

import PySimpleGUI as sg
from pydantic import create_model
from pydantic.error_wrappers import ValidationError as ValidateError
from PyInquirer import (Token, Validator, prompt, style_from_dict)

custom_style_1 = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

custom_style_2 = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    # Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

custom_style_3 = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


def check_type(obj, _type):
    # only process 2 level inner
    origin_type = getattr(_type, '__origin__', _type)
    if not isinstance(obj, origin_type):
        return False
    key_type, value_type, *_ = getattr(_type, '__args__',
                                       (object,)) + (object, object)
    if origin_type is dict:
        for k, v in obj.items():
            if not (isinstance(k, key_type) and isinstance(v, value_type)):
                return False
    elif origin_type is list:
        for v in obj:
            if not isinstance(v, value_type):
                return False
    return True


class Param(object):
    __slots__ = ('name', 'kind', 'annotation', 'default')

    def __init__(self, name, kind, annotation=..., default=...):
        self.name = name
        self.kind = kind
        self.annotation = annotation
        self.default = default

    def __str__(self):
        return f'Param(name={self.name}, kind={self.kind}, annotation={self.annotation}, default={self.default})'


class BaseSchema(object):
    sep_sig = f'{"=" * 40}\n'
    valid_types = {list, int, bool, str, tuple, set, float, dict}
    NOT_SUPPORT_KIND = {Parameter.POSITIONAL_ONLY, Parameter.VAR_POSITIONAL}

    def __init__(self,
                 function,
                 choices: Dict[str, list] = None,
                 checkboxes: Dict[str, list] = None,
                 defaults: Dict[str, Any] = None,
                 custom_style: Dict = None,
                 read_doc: bool = True,
                 use_raw_list: bool = False):
        """Set the function and ask for args with REPL mode.

        :param function: callable function
        :type function: callable
        :param choices: default choices for some variables, use it like {'arg_name': [1, 2, 3]}, defaults to None
        :type choices: Dict[str, list], optional
        :param checkboxes: multi-choice values for some variables, use it like {'arg_name': [1, 2, 3]}, defaults to None
        :type checkboxes: Dict[str, list], optional
        :param defaults: default values for some difficultly-input variables object, use it like {'arg_name': SomeComplexObject}, defaults to None
        :type defaults: Dict[str, list], optional
        """
        if not callable(function):
            raise ValueError
        self.function = function
        self.varkw_name = None
        self.custom_style = custom_style
        self.use_raw_list = use_raw_list
        self.choices = choices or {}
        self.checkboxes = checkboxes or {}
        self.defaults = defaults or {}
        self.share_kwargs: Dict[str, Any] = {}

    def validate(self, key, text):
        try:
            self.share_kwargs[key] = text
            self.FuncSchema(**self.share_kwargs)
            return True
        except ValidateError as err:
            return f'{err}'.replace('\n', ' ')

    def gen_validator(self, key):
        return partial(self.validate, key)

    def run(self, kwargs=None):
        if kwargs is None:
            kwargs = self.ask_for_args()
        if self.varkw_name:
            varkw = kwargs.pop(self.varkw_name, {})
            kwargs.update(varkw)
        func_to_run = f'{self.function.__name__}(**{kwargs})'
        print(f'{self.sep_sig}Start to run {func_to_run}\n{self.sep_sig}')
        result = self.function(**kwargs)
        print(
            f'{self.sep_sig}{func_to_run} and return {type(result)}:\n{result}')

    def ask_for_args(self, *args, **kwargs):
        raise NotImplementedError

    def print_doc(self, value):
        doc = self.function.__doc__
        if value:
            if doc.strip():
                print(f'Documentary:\n{doc}')
            else:
                print('no doc.')
        return value

    def empty_to_ellipsis(self, obj, default=...):
        if obj is Parameter.empty:
            return default
        else:
            return obj

    def get_type_null(self, _type, default=''):
        if _type in (Parameter.empty, ...):
            return default
        otype = getattr(_type, '__origin__', _type)
        try:
            if callable(otype):
                return otype()
            else:
                return default
        except TypeError:
            return default

    @property
    def schema_args(self):
        return self.make_schema()

    def make_schema(self):
        sig = inspect.signature(self.function)
        print(
            f'{self.sep_sig}Preparing {self.function.__name__}{sig}\n{self.sep_sig}'
        )
        kwargs: List[Parameter] = []
        for param in sig.parameters.values():
            if param.kind == Parameter.VAR_KEYWORD:
                self.varkw_name = param.name
            if param.kind in self.NOT_SUPPORT_KIND:
                print(
                    f'not support {self.NOT_SUPPORT_KIND}, variable {param} will be ignored.'
                )
                continue
            kwargs.append(
                Param(param.name, param.kind,
                      self.empty_to_ellipsis(param.annotation, str),
                      {} if param.kind == Parameter.VAR_KEYWORD else
                      self.empty_to_ellipsis(
                          param.default, self.get_type_null(param.annotation))))
        model_kwargs = {p.name: (p.annotation, p.default) for p in kwargs}
        self.FuncSchema = create_model('FuncSchema', **model_kwargs)

        return kwargs

    def __str__(self):
        return f'{self.__class__.__name__}{self.schema_args}'


class Ask4Args(BaseSchema):
    """Terminal UI automatic generator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_input_decorator(self, param, kw=False):
        """kw means Dict handler."""

        def wrap(is_using_default):
            # nonlocal param
            ops = param.annotation.__args__ or (str, str)
            type_func1 = ops[0]
            if kw:
                type_func2 = ops[1]
            if is_using_default and param.default is not Parameter.empty:
                if check_type(param.default, param.annotation):
                    return param.default
                else:
                    print(
                        f'default value `{param.default}` not fit {param.annotation}, you can set default by self.defaults.'
                    )
            print('Invalid default value, should input one by one.')
            if kw:
                result = {}
            else:
                result = []
            while 1:
                if kw:
                    key = input('Input the dict\'s key(null for break): ')
                    if not key.strip():
                        break
                    key = type_func1(key) if callable(type_func1) else key
                    try:
                        key = type_func1(key) if callable(type_func1) else key
                    except ValueError:
                        print(f'bad value {key}, {type_func1} needed.')
                        continue
                    value = input('Input the dict\'s value: ')
                    try:
                        value = type_func2(value) if callable(
                            type_func2) else value
                    except ValueError:
                        print(f'bad value {value}, {type_func2} needed.')
                        continue
                    result[key] = value
                else:
                    value = input('Input the list\'s value(null for break): ')
                    if not value.strip():
                        break
                    try:
                        value = type_func1(value) if callable(
                            type_func1) else value
                    except ValueError:
                        print(f'bad value {value}, {type_func1} needed.')
                        continue
                    result.append(value)
            self.share_kwargs[param.name] = result
            return result

        return wrap

    def make_question(self, param) -> Dict:
        if param.default is Parameter.empty:
            default_template = '[required]'
        else:
            default_template = f'default to {param.default}'
        msg = f'Input the value of `{param.name}` ({default_template};) {param.annotation}:'
        question = {
            # 'qmark': self.sep_sig,
            'type': 'input',
            'name': param.name,
            'message': msg,
            'validate': self.gen_validator(param.name),
        }
        origin_type = getattr(param.annotation, '__origin__', param.annotation)
        if isinstance(param.default, (origin_type,)) and param.default:
            question['default'] = str(param.default)
        else:
            question['default'] = ''
        if param.name in self.choices:
            if self.use_raw_list:
                question['type'] = 'rawlist'
            else:
                question['type'] = 'list'
            question['choices'] = [{
                'name': str(item),
                'value': item
            } for item in self.choices[param.name]]
            # question.pop('validate', None)
        elif origin_type is bool:
            question['type'] = 'confirm'
        elif origin_type in {list, tuple, set}:
            if self.use_raw_list:
                question['type'] = 'rawlist'
            else:
                question['type'] = 'list'
            if param.name in self.checkboxes:
                question['type'] = 'checkbox'
                question.pop('default', None)
                question['choices'] = [{
                    'name': str(item),
                    'value': item
                } for item in self.checkboxes[param.name]]
            else:
                question['type'] = 'confirm'
                question[
                    'message'] += f'\nThere is no choice / checkbox, use the default value `{param.default}`(press Y / enter) or input your custom value(press N)'
                question['filter'] = self.handle_input_decorator(param)
        elif origin_type is dict:
            question['type'] = 'confirm'
            question[
                'message'] += f'\nThere is no choice / checkbox, use the default value [{param.default}](press Y / enter) or input your custom value(press N)'
            question['filter'] = self.handle_input_decorator(param, kw=True)
        return question

    def deal_with_arg(self, param: Parameter, questions: List):
        if param.name in self.defaults:
            # use default value instead, no need to ask question
            self.share_kwargs[param.name] = self.defaults[param.name]
        else:
            # ask for param value
            question = self.make_question(param)
            if question:
                questions.append(question)

    def ask_for_args(self):
        kwargs: dict = self.schema_args
        questions = []
        if self.function.__doc__:
            questions.append({
                'type': 'confirm',
                'name': '_ask4args_ignore_name',
                'message': 'Would you want to read the function doc?',
                'default': False,
                'filter': self.print_doc
            })
        for param in kwargs:
            self.deal_with_arg(param, questions)
        answers = prompt(questions, style=self.custom_style)
        answers.pop('_ask4args_ignore_name', None)
        self.share_kwargs.update(answers)
        self.share_kwargs = self.FuncSchema(**self.share_kwargs).dict()
        return self.share_kwargs


class Ask4ArgsGUI(BaseSchema):
    """GUI automatic generator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        pass

    def ask_for_args(self):
        args: dict = self.schema_args


class Ask4ArgsWeb(BaseSchema):
    """GUI automatic generator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError


if __name__ == "__main__":

    def test(a,
             b: int = 2,
             *,
             c: bool = False,
             d: str = 'string',
             e: int = None,
             f: List[int] = None,
             **args_dict: Dict[str, int]):
        """doc"""
        pass

    print(Ask4Args(test).run())
