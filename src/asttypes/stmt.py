from __future__ import annotations
from abc import ABC, abstractmethod
import enum
from typing import TypeVar

from asttypes.astnode import ASTNode
from asttypes.expr import Expr
from asttypes.stmtvisitor import StmtVisitor


T = TypeVar('T')

class Stmt(ASTNode, ABC):
    class Type(enum.Enum):
        Brace   = enum.auto()
        Expr    = enum.auto()
        Decl    = enum.auto()
        If      = enum.auto()
        While   = enum.auto()
        For     = enum.auto()


    def __init__(self, type: Type) -> None:
        self.type = type


    @abstractmethod
    def accept(self, visitor: StmtVisitor[T]) -> T:
        raise NotImplementedError()


class BlockStmt(Stmt):
    def __init__(self, stmts: list[Stmt]) -> None:
        super().__init__(Stmt.Type.Brace)
        self.stmts = stmts


    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_brace_stmt(self)


class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        super().__init__(Stmt.Type.Expr)
        self.expr = expr


    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_expr_stmt(self)


class IfStmt(Stmt):
    def __init__(self, cond: Expr, thenbranch: Stmt, elsebranch: Stmt | None) -> None:
        super().__init__(Stmt.Type.If)
        self.cond = cond
        self.thenbranch = thenbranch
        self.elsebranch = elsebranch


    def accept(self, visitor: StmtVisitor[T]) -> T:
        return super().accept(visitor)


class WhileStmt(Stmt):
    def __init__(self, cond: Expr, body: Stmt) -> None:
        super().__init__(Stmt.Type.While)
        self.cond = cond
        self.body = body


    def accept(self, visitor: StmtVisitor[T]) -> T:
        return super().accept(visitor)
