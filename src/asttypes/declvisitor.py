from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from asttypes import decl


T = TypeVar('T')

class DeclVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_let(self, let: decl.LetDecl) -> T:
        raise NotImplementedError()


    @abstractmethod
    def visit_func(self, func: decl.FuncDecl) -> T:
        raise NotImplementedError()
