import sys
from abc import ABC, abstractmethod
from pathlib import Path
from PyInquirer import *

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
    #Token.Selected: '',  # default
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


def choose_class():
    argv = sys.argv
    if len(argv) < 2:
        raise IOError('please input the class name')
    name = argv[1]
    for cls in BaseClass.__subclasses__():
        if cls.name.lower() == name:
            return cls
    else:
        print(f'not found class {name}')


class BaseClass(ABC):
    home_path = Path.home()

    @abstractmethod
    def run(self):
        pass


class ExampleClass(BaseClass):

    def run(self):
        questions = [
            {
                'type': 'input',
                'name': 'first_name',
                'message': 'What\'s your first name',
            },
        ]
        answers = prompt(questions)
        print(answers)
        # {'first_name': ''}


class TempVenv(BaseClass):

    def run(self):
        import venv
        questions = [
            {
                'type': 'confirm',
                'message': 'a Boolean value indicating that the system Python site-packages should be available to the environment.',
                'name': 'system_site_packages',
                'default': False,
            },
            {
                'type': 'confirm',
                'message': 'a Boolean value which, if true, will delete the contents of any existing target directory, before creating the environment.',
                'name': 'clear',
                'default': False,
            },
            {
                'type': 'confirm',
                'message': 'a Boolean value indicating whether to attempt to symlink the Python binary rather than copying.',
                'name': 'symlinks',
                'default': False,
            },
            {
                'type': 'confirm',
                'message': 'a Boolean value which, if true, will upgrade an existing environment with the running Python - for use when that Python has been upgraded in-place.',
                'name': 'upgrade',
                'default': False,
            },
            {
                'type': 'confirm',
                'message': 'a Boolean value which, if true, ensures pip is installed in the virtual environment.',
                'name': 'with_pip',
                'default': False,
            },
            {
                'type': 'confirm',
                'message': 'a String to be used after virtual environment is activated (defaults to None which means directory name of the environment would be used).',
                'name': 'prompt',
                'default': False,
            },
        ]
        answers = prompt(questions, style=custom_style_1)
        print(answers)
        # {'first_name': ''}


if __name__ == "__main__":
    t = TempVenv()
    t.run()
