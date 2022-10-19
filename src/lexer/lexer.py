from curses import ascii

from core.tokenkind import TokenKind
from lexer.keywords import KEYWORDS
from lexer.token import Token


class Lexer:
    def __init__(self, str: str) -> None:
        self.str = str
        self.tokens: list[Token] = []
        self.current: int = 0


    def peek(self) -> str:
        if self.current == len(self.str):
            return ''
        return self.str[self.current + 1]


    def consume(self) -> str:
        ch = self.str[self.current]
        self.current += 1
        return ch


    def lex_number(self, start: int) -> None:
        str_len: int = len(self.str)

        i: int = start
        while ascii.isdigit(self.str[i]):
            i += 1
            if i == str_len:
                break

        self.current += i - start

        tok: Token = Token(TokenKind.Number)
        tok.set_literal_data(self.str[start:i])

        self.tokens.append(tok)


    def lex_identifier(self, start: int) -> None:
        str_len: int = len(self.str)

        i: int = start
        while ascii.isalnum(self.str[i]) or self.str[i] == '_':
            i += 1
            if i == str_len:
                break

        self.current += i - start
        ident: str = self.str[start:i]

        # check for valid keywords
        kind = KEYWORDS.get(ident)

        if kind == None:
            tok: Token = Token(TokenKind.Identifier)
            tok.set_identifier_data(ident)
        else:
            tok: Token = Token(kind)

        self.tokens.append(tok)


    # Main lexer loop
    def lex(self) -> None:
        str_len: int = len(self.str)

        while (self.current < str_len):
            c: str = self.str[self.current]

            # New-line
            if c == '\n':
                self.current += 1

            # Whitespaces
            elif ascii.isspace(c):
                self.current += 1

            # Number
            elif ascii.isdigit(c):
                self.lex_number(self.current)

            # Identifiers
            elif ascii.isalnum(c) or c == '_':
                self.lex_identifier(self.current)

            # Operators
            elif c == '+':
                self.tokens.append(
                    Token(TokenKind.Op_Plus))
                self.current += 1
            elif c == '-':
                self.tokens.append(
                    Token(TokenKind.Op_Minus))
                self.current += 1
            elif c == '*':
                self.tokens.append(
                    Token(TokenKind.Op_Star))
                self.current += 1
            elif c == '/':
                self.tokens.append(
                    Token(TokenKind.Op_Slash))
                self.current += 1
            elif c == '{':
                self.tokens.append(
                    Token(TokenKind.Op_LBrace))
                self.current += 1
            elif c == '}':
                self.tokens.append(
                    Token(TokenKind.Op_RBrace))
                self.current += 1
            elif c == '(':
                self.tokens.append(
                    Token(TokenKind.Op_LParen))
                self.current += 1
            elif c == ')':
                self.tokens.append(
                    Token(TokenKind.Op_RParen))
                self.current += 1
            elif c == '=':
                ch = self.peek()
                if ch == '=':
                    self.tokens.append(
                        Token(TokenKind.Op_EqualEqual))
                    self.current += 2
                else:
                    self.tokens.append(
                        Token(TokenKind.Op_Equal))
                    self.current += 1
            elif c == '!':
                ch = self.peek()
                if ch == '=':
                    self.tokens.append(
                        Token(TokenKind.Op_ExclaimEqual))
                    self.current += 2
                else:
                    self.tokens.append(
                        Token(TokenKind.Op_Exclaim))
                    self.current += 1
            elif c == '<':
                ch = self.peek()
                if ch == '=':
                    self.tokens.append(
                        Token(TokenKind.Op_LessEqual))
                    self.current += 2
                else:
                    self.tokens.append(
                        Token(TokenKind.Op_Less))
                    self.current += 1
            elif c == '>':
                ch = self.peek()
                if ch == '=':
                    self.tokens.append(
                        Token(TokenKind.Op_GreaterEqual))
                    self.current += 2
                else:
                    self.tokens.append(
                        Token(TokenKind.Op_Greater))
                    self.current += 1
            elif c == ',':
                self.tokens.append(
                    Token(TokenKind.Op_Comma))
                self.current += 1

        self.tokens.append(Token(TokenKind.End))
