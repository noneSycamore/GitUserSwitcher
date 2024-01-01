import argparse

from CustomUtils import changeColor

class CheckSave(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 2 <= len(values) <= 3:
            print(changeColor("The --save option requires 2 or 3 arguments.", 'red'))
            return
        setattr(namespace, self.dest, values)

class CheckEdit(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != 3:
            print(changeColor("The --edit option requires 3 arguments.", 'red'))
            return
        setattr(namespace, self.dest, values)
