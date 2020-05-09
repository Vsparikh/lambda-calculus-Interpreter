from Interpreter import *

def repl():
    while True:
        prog = input(">> ")
        if prog == 'QUIT':
            break
        res = Interp.interp(Parser.parseProgram(prog))
        print(res)

if __name__ == '__main__':
    repl()
    