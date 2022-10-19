from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from asttypes import stmt


T = TypeVar('T')

class StmtVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_brace_stmt(self, block: stmt.BlockStmt) -> T:
        raise NotImplementedError()


    @abstractmethod
    def visit_expr_stmt(self, expr: stmt.ExprStmt) -> T:
        raise NotImplementedError()
