#!/usr/bin/env python3

import sys
from asttypes.expr import Expr

from lexer.lexer import Lexer
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
        print(f"Failed to open {filename}: {e.args[1]}!")
        sys.exit(e.args[0])

    # lexer invoking
    lexer: Lexer = Lexer(data)
    lexer.lex()

    # parser invoking
    parser: Parser = Parser(lexer.tokens)
    expr: Expr | None = parser.parse() # type: ignore

    print("Done")


if __name__ == '__main__':
    main()
