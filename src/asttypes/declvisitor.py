from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from asttypes import decl


T = TypeVar('T')

class DeclVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_let(self, let_decl: decl.LetDecl) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_func(self, func_decl: decl.FuncDecl) -> T:
        raise NotImplementedError()
