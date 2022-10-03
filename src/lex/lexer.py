from curses import ascii
from lex.tokenkind import TokenKind
from lex.token import Token


class Lexer:
    def __init__(self, str) -> None:
        self.str = str
        self.tokens: list[Token] = []
        self.current: int = 0


    def peek(self) -> str:
        if self.current == len(self.str): return ''
        return self.str[self.current + 1]


    def consume(self) -> str:
        ch = self.str[self.current]
        self.current += 1
        return ch


    def lex_number(self, start) -> None:
        str_len: int = len(self.str)
        i: int = start
        while ascii.isdigit(self.str[i]):
            i += 1
            if (i == str_len):
                break

        self.current += i - start
        tok: Token = Token(TokenKind.Number)
        tok.set_data(self.str[start:i])
        self.tokens.append(tok)


    def lex_identifier(self, start) -> None:
        str_len: int = len(self.str)
        i: int = start
        while ascii.isalnum(self.str[i]):
            i += 1
            if (i == str_len):
                break

        self.current += i - start
        tok: Token = Token(TokenKind.Identifier)
        tok.set_data(self.str[start:i])
        self.tokens.append(tok)


    def lex(self) -> None:
        str_len = len(self.str)

        while (self.current < str_len):
            c = self.str[self.current]

            # New-lines
            if c == '\n':
                self.current += 1

            # Whitespaces
            elif ascii.isspace(c):
                self.current += 1

            # Number
            elif ascii.isdigit(c):
                self.lex_number(self.current)

            elif ascii.isalpha(c) or c == '_':
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

        self.tokens.append(Token(TokenKind.End))
