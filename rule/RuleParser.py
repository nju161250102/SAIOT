import json
import logging


class RuleParser:
    def __init__(self, rule):
        if isinstance(rule, str):
            self.rule = json.loads(rule)
        else:
            self.rule = rule
        self.validate(self.rule)

    class Functions(object):

        ALIAS = {
            '=': 'eq',
            '!=': 'neq',
            '>': 'gt',
            '>=': 'gte',
            '<': 'lt',
            '<=': 'lte',
            'and': 'and_',
            'in': 'in_',
            'or': 'or_',
            'not': 'not_',
            'int': 'int_',
            '+': 'plus',
            '-': 'minus',
            '*': 'multiply',
            '/': 'divide',
            '%': 'mod'
        }

        def eq(self, *args):
            return args[0] == args[1]

        def neq(self, *args):
            return args[0] != args[1]

        def in_(self, *args):
            return args[0] in args[1:]

        def gt(self, *args):
            return args[0] > args[1]

        def gte(self, *args):
            return args[0] >= args[1]

        def lt(self, *args):
            return args[0] < args[1]

        def lte(self, *args):
            return args[0] <= args[1]

        def not_(self, *args):
            return not args[0]

        def or_(self, *args):
            return any(args)

        def and_(self, *args):
            return all(args)

        def int_(self, *args):
            return int(args[0])

        def upper(self, *args):
            return args[0].upper()

        def lower(self, *args):
            return args[0].lower()

        def plus(self, *args):
            return sum(args)

        def minus(self, *args):
            return args[0] - args[1]

        def multiply(self, *args):
            return args[0] * args[1]

        def divide(self, *args):
            return float(args[0]) / float(args[1])

        def mod(self, *args):
            return int(args[0]) % int(args[1])

    @staticmethod
    def validate(rule):
        if not isinstance(rule, list):
            logging.error('Rule must be a list, got {}'.format(type(rule)))
        if len(rule) < 2:
            logging.error('Must have at least one argument.')

    def _evaluate(self, rule, fns: Functions, data: dict):
        """
        递归执行list内容
        """
        def _recurse_eval(arg):
            if isinstance(arg, list):
                return self._evaluate(arg, fns, data)
            else:
                return data[arg] if arg in data.keys() else arg

        r = list(map(_recurse_eval, rule))
        r[0] = self.Functions.ALIAS.get(r[0]) or r[0]
        func = getattr(fns, r[0])
        return func(*r[1:])

    def evaluate(self, data):
        fns = self.Functions()
        ret = self._evaluate(self.rule, fns, data)
        if not isinstance(ret, bool):
            logging.warning('In common usage, a rule must return a bool value, '
                            'but get {}, please check the rule to ensure it is true')
        return ret
