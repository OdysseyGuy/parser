from abc import ABC, abstractmethod
import enum
from typing import TypeVar

from asttypes.astnode import ASTNode
from asttypes.declvisitor import DeclVisitor
from asttypes.expr import Expr
from asttypes.paramlist import ParamList
from asttypes.stmt import BlockStmt

from lexer.token import Token


T = TypeVar('T')

class Decl(ASTNode, ABC):
    """Base class for all types of declarations."""

    class Type(enum.Enum):
        Invalid = enum.auto()
        Let     = enum.auto()
        Func    = enum.auto()
        Class   = enum.auto()

    def __init__(self, type: Type) -> None:
       self.type = type

    @abstractmethod
    def accept(self, visitor: DeclVisitor[T]) -> T:
        raise NotImplementedError()


class InvalidDecl(Decl):
    """Erroneous declaration."""

    def __init__(self) -> None:
        super().__init__(Decl.Type.Invalid)

    def accept(self, visitor: DeclVisitor[T]) -> T:
        raise Exception("Visiting invalid declaration.")


class LetDecl(Decl):
    """A 'let' variable declaration."""

    def __init__(self, name: Token, initializer: Expr | None) -> None:
        super().__init__(Decl.Type.Let)
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: DeclVisitor[T]) -> T:
        return visitor.visit_let(self)


class AbstractFuncDecl(Decl, ABC):
    """Base class for function-like declarations."""

    def __init__(self, params: ParamList, body: BlockStmt) -> None:
        super().__init__(Decl.Type.Func)
        self.params = params
        self.body = body


class FuncDecl(AbstractFuncDecl):
    """A 'func' declaration."""

    def __init__(
        self,
        name: Token,
        params: ParamList,
        body: BlockStmt
    ) -> None:
        super().__init__(params, body)
        self.name = name

    def accept(self, visitor: DeclVisitor[T]) -> T:
        return visitor.visit_func(self)


class ClassDecl(Decl):
    def __init__(self, name: Token, inherited: list[Token]) -> None:
        super().__init__(Decl.Type.Class)
        self.name = name

    def accept(self, visitor: DeclVisitor[T]) -> T:
        return super().accept(visitor)
