class Lambda:
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __repr__(self):
        return f'\u03BB{self.param}. {self.body}'

    def __str__(self):
         return f'\u03BB{self.param}. {self.body}'

class App:
    def __init__(self, fn, arg):
        self.fn = fn
        self.arg= arg

    def __repr__(self):
        return f'(({self.fn}) {self.arg})'

    def __str__(self):
        return  f'(({self.fn}) {self.arg})'

class Parser:
    @staticmethod
    def parseProgram(program):
        return Parser.parse(Parser.make_syntax_tree(Parser.tokenize(program)))

    @staticmethod
    def tokenize(prog):
        return prog.replace('(', ' ( ').replace(')', ' ) ').split()

    @staticmethod
    def create_atoms(token):
        try: return int(token)
        except ValueError:
            try: return float(token)
            except ValueError:
                return str(token)
    
    @staticmethod
    def isNum(number):
        if number == None:
            return False
        try: 
            int(number)
            return True
        except ValueError: 
            try:
                float(number)
                return True
            except ValueError:
                return False
    
    @staticmethod
    def make_syntax_tree(tokens):
        if len(tokens) == 0:
            raise SyntaxError('parser encountered unexpected EOF')
        elif tokens[0] == ')':
            raise SyntaxError('parser encountered unexpected ")"')
        elif tokens[0] == '(':
            tokens.pop(0) # remove '('
            L = []
            while tokens[0] != ')':
                L.append(Parser.make_syntax_tree(tokens))
            tokens.pop(0)# remove ')'
            return L
        else:
            return Parser.create_atoms(tokens.pop(0))

    @staticmethod
    def parse(ast):
        if isinstance(ast, (float, str, int)):
            return ast
        if len(ast) == 1: 
            if isinstance(ast, list): # list of list
                return Parser.parse(ast[0])
            else:                     # variable
                return ast[0]
        elif len(ast) == 3:           # function
            if ast[0] != 'lambda':
                raise SyntaxError('Parser encountered Syntax Error')
            
            if Parser.isNum(ast[1]):
                raise SyntaxError(f'cannot use {ast[1]} as Variable')
            
            ast.pop(0) # remove lambda
            param = ast.pop(0) # parameter
            body = Parser.parse(ast.pop(0))
            return Lambda(param, body)

        elif len(ast) == 2:
            fn = Parser.parse(ast[0])
            arg = Parser.parse(ast[1])

            if not isinstance(fn, (App, Lambda)):
                raise SyntaxError('Parser encountered application error') 
            return App(fn, arg)


class Interp:
    @staticmethod
    def interp(ast):
        if isinstance(ast, (float,int, str, Lambda)):
            return ast
        elif isinstance(ast, App):
            fn = Interp.interp(ast.fn)
            arg = Interp.interp(ast.arg)
            if not isinstance(fn, Lambda):
                raise SyntaxError('Interp encountered application error') 

            return Interp.subst(fn.param,arg, fn.body)

    @staticmethod
    def subst(var, val, expr):
        if isinstance(expr, (int, float)):
            return expr
        elif isinstance(expr, str):
            if expr == var:
                return val
            else:
                return expr
        elif isinstance(expr, Lambda):
            if expr.param == var:
                return expr
            else:
                expr.body = Interp.subst(var, val, expr.body)
                return expr
        elif isinstance(expr, App):
            expr.fn = Interp.subst(var, val, expr.fn)
            expr.arg = Interp.subst(var, val, expr.arg)

        
if __name__ == '__main__':
    inp = input()
    res = Interp.interp(Parser.parseProgram(inp))
    print(res)
   