from __future__ import annotations
from abc import ABC, abstractmethod
import enum
from typing import Optional, TypeVar

from asttypes.astnode import ASTNode
from asttypes.expr import Expr
from asttypes.stmtvisitor import StmtVisitor


T = TypeVar('T')

class Stmt(ASTNode, ABC):
    """Base class for different types of statements."""

    class Type(enum.Enum):
        Brace   = enum.auto()
        Expr    = enum.auto()
        If      = enum.auto()
        While   = enum.auto()
        Return  = enum.auto()

    def __init__(self, type: Type) -> None:
        self.type = type

    @abstractmethod
    def accept(self, visitor: StmtVisitor[T]) -> T:
        raise NotImplementedError()


class BlockStmt(Stmt):
    """Represents a '{' ... '}' block."""

    def __init__(self, elems: list[ASTNode]) -> None:
        # TODO: Should be a more fundamental type for this method
        #       to support declarations, statments and expressions
        #       together.
        super().__init__(Stmt.Type.Brace)
        self.elems = elems

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_block_stmt(self)


class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        super().__init__(Stmt.Type.Expr)
        self.expr = expr

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_expr_stmt(self)


class IfStmt(Stmt):
    """If statement."""

    def __init__(
        self,
        cond: Expr,
        thenbranch: Stmt,
        elsebranch: Optional[Stmt]
    ) -> None:
        """Creates an if statement.

        Args:
            cond: Conditional Expression.
            thenbranch: True branch.
            elsebrach: False branch.
        """
        super().__init__(Stmt.Type.If)
        self.cond = cond
        self.thenbranch = thenbranch
        self.elsebranch = elsebranch

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_if_stmt(self)


class WhileStmt(Stmt):
    """While statement."""

    def __init__(self, cond: Expr, body: Stmt) -> None:
        super().__init__(Stmt.Type.While)
        self.cond = cond
        self.body = body

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_while_stmt(self)


class ReturnStmt(Stmt):
    """Return statement."""

    def __init__(
        self,
        expr: Expr,
        cond: Optional[Expr]
    ) -> None:
        super().__init__(Stmt.Type.Return)
        self.expr = expr
        self.cond = cond

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_return_stmt(self)
