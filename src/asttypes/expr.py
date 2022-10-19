from __future__ import annotations
from abc import ABC
import enum

from asttypes.astnode import ASTNode
from core.ops import BinaryOp, UnaryOp
from lexer.token import Token


class Expr(ASTNode, ABC):
    class Type(enum.Enum):
        Invalid     = enum.auto()
        Assign      = enum.auto()
        Call        = enum.auto()
        Unary       = enum.auto()
        Binary      = enum.auto()
        Literal     = enum.auto()
        Group       = enum.auto()
        Variable    = enum.auto()


    def __init__(self, type: Type) -> None:
        self.type = type


class InvalidExpr(Expr):
    def __init__(self) -> None:
        super().__init__(Expr.Type.Invalid)


class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        super().__init__(Expr.Type.Assign)
        self.name = name
        self.value = value


class CallExpr(Expr):
    def __init__(self, callee: Expr, args: list[Expr]) -> None:
        super().__init__(Expr.Type.Call)
        self.callee = callee
        self.args = args


class VariableExpr(Expr):
    def __init__(self, name: Token) -> None:
        super().__init__(Expr.Type.Variable)
        self.name = name


class BinaryExpr(Expr):
    def __init__(self, lhs: Expr, op: BinaryOp, rhs: Expr) -> None:
        super().__init__(Expr.Type.Binary)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class UnaryExpr(Expr):
    def __init__(self, op: UnaryOp, expr: Expr) -> None:
        super().__init__(Expr.Type.Unary)
        self.op = op
        self.expr = expr


class GroupExpr(Expr):
    def __init__(self, expr: Expr) -> None:
        super().__init__(Expr.Type.Group)
        self.expr = expr


class LiteralExpr(Expr):
    def __init__(self, literal: str) -> None:
        super().__init__(Expr.Type.Literal)
        self.literal = literal
