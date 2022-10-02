from lex.token import Token
from lex.tokenkind import TokenKind
from parser.expr import BinaryExpr, Expr, GroupExpr, LiteralExpr, UnaryExpr

'''
Expression Grammar.

Precedence      Associativity
----------      -------------
Sum    (+, -)   Left
Factor (*, /)   Left
Unary  (-)      Right


Removing left-recursion from grammar
------------------------------------
s -> s + f | f
s -> f (+ f)*


Grammer
-------
expression  -> term+
term        -> term ('+' | '-') factor
            | factor
factor      -> factor ('/' | '*') unary
            | unary
unary       -> ('-') unary
            | primary
primary     -> number
            | '(' expression ')'


Grammar (without left-recursion)
--------------------------------
expression  -> term+
term        -> factor (('+' | '-') factor)*
factor      -> unary (('/' | '*') unary)*
unary       -> ('-') unary
            | primary
primary     -> number
            | '(' expression ')'

'''


class Parser:
    def __init__(self, tokens: 'list[Token]') -> None:
        self.tokens: list[Token] = tokens
        self.current: int = 0


    def peek(self) -> Token:
        return self.tokens[self.current]


    def previous(self) -> Token:
        return self.tokens[self.current - 1]


    def is_at_end(self) -> bool:
        return self.peek().is_of_kind(TokenKind.End)


    def consume(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()


    def must_consume(self, kind: TokenKind, message: str):
        if (self.check(kind)): return self.consume()
        else:
            raise Exception(message)


    def check(self, kind: TokenKind) -> bool:
        if self.is_at_end(): return False
        return self.peek().is_of_kind(kind)


    def match(self, *tok_kinds: TokenKind) -> bool:
        '''
        Returns true if the next token kind matches anyone of
        the provided token kinds.
        '''
        for kind in tok_kinds:
            if self.check(kind):
                self.consume()
                return True

        return False


    # ----------------------- Expressions -----------------------
    def expr(self) -> Expr:
        return self.term_expr()


    def term_expr(self):
        expr: Expr = self.factor_expr()

        while (self.match(TokenKind.Op_Plus, TokenKind.Op_Minus)):
            # already consumed in match()
            op: Token = self.previous()
            right: Expr = self.factor_expr()
            expr = BinaryExpr(expr, op, right)

        return expr


    def factor_expr(self):
        expr: Expr = self.unary_expr()

        while (self.match(TokenKind.Op_Slash, TokenKind.Op_Star)):
            op: Token = self.previous()
            right: Expr = self.unary_expr()
            expr = BinaryExpr(expr, op, right)

        return expr


    def unary_expr(self):
        if (self.match(TokenKind.Op_Minus)):
            op: Token = self.previous()
            right: Expr = self.unary_expr()
            return UnaryExpr(op, right)

        return self.primary_expr()


    def primary_expr(self):
        if (self.match(TokenKind.Number)):
            return LiteralExpr(self.previous().get_literal_data())

        if (self.match(TokenKind.Op_LParen)):
            expr: Expr = self.expr()
            self.must_consume(TokenKind.Op_RParen, "Expected ')' after expression.")
            return GroupExpr(expr)


    def parse(self):
        try:
            return self.expr()
        except Exception as e:
            print(f"Error: {str(e)}")
