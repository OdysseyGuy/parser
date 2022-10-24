from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from asttypes import stmt


T = TypeVar('T')

class StmtVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_block_stmt(self, block_stmt: stmt.BlockStmt) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_expr_stmt(self, expr_stmt: stmt.ExprStmt) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_if_stmt(self, if_stmt: stmt.IfStmt) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_while_stmt(self, while_stmt: stmt.WhileStmt) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_return_stmt(self, return_stmt: stmt.ReturnStmt) -> T:
        raise NotImplementedError()
