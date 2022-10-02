import enum
from lex.token import Token


class Expr:
    class Type(enum.Enum):
        Invalid = 0
        Unary = 1
        Binary = 2
        Literal = 3
        Group = 4


    def __init__(self, type: Type) -> None:
        self.type = type


class BinaryExpr(Expr):
    def __init__(self, lhs: Expr, op: Token, rhs: Expr) -> None:
        super().__init__(Expr.Type.Binary)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class UnaryExpr(Expr):
    def __init__(self, op: Token, right: Expr) -> None:
        super().__init__(Expr.Type.Unary)
        self.op = op
        self.right = right


class GroupExpr(Expr):
    def __init__(self, expr: Expr) -> None:
        super().__init__(Expr.Type.Group)
        self.expr = expr


class LiteralExpr(Expr):
    def __init__(self, literal: str) -> None:
        super().__init__(Expr.Type.Literal)
        self.literal = literal
