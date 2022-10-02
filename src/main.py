#!/usr/bin/env python3

import sys
from lex.lexer import Lexer
from parser.expr import Expr
from parser.parser import Parser


def main():
    # argc = len(sys.argv)
    filename: str = 'test/main.ar'

    # if argc >= 2:
    #     filename = sys.argv[1]
    # else:
    #     sys.exit(1)

    # read file
    data: str = ''
    try:
        with open(filename, 'r') as file:
            data = file.read()
    except Exception as e:
        print(f"Failed to open '{filename}': {e.args[1]}!")
        sys.exit(e.args[0])

    # lexer invoking
    lexer: Lexer = Lexer(data)
    lexer.lex()

    for token in lexer.tokens:
        print(token)

    return

    # parser invoking
    parser: Parser = Parser(lexer.tokens)
    expr: Expr = parser.parse()


if __name__ == '__main__':
    main()