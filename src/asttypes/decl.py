from abc import ABC, abstractmethod
import enum
from typing import TypeVar
import typing

from asttypes.astnode import ASTNode
from asttypes.declvisitor import DeclVisitor
from asttypes.expr import Expr
from asttypes.paramlist import ParamList

from lexer.token import Token

if typing.TYPE_CHECKING:
    from asttypes.stmt import BlockStmt


T = TypeVar('T')

class Decl(ASTNode, ABC):
    class Type(enum.Enum):
        Invalid = enum.auto()
        Let     = enum.auto()
        Func    = enum.auto()


    def __init__(self, type: Type) -> None:
       self.type = type


    @abstractmethod
    def accept(self, visitor: DeclVisitor[T]) -> T:
        raise NotImplementedError()


class InvalidDecl(Decl):
    '''
    Erroneous declaration.
    '''
    def __init__(self) -> None:
        super().__init__(Decl.Type.Invalid)


    def accept(self, visitor: DeclVisitor[T]) -> T:
        raise Exception("Visiting invalid declaration.")


class LetDecl(Decl):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        super().__init__(Decl.Type.Let)
        self.name = name
        self.initializer = initializer


    def accept(self, visitor: DeclVisitor[T]) -> T:
        return visitor.visit_let(self)


class AbstractFuncDecl(Decl, ABC):
    '''
    Base class for function-like declarations.
    '''
    def __init__(self, params: ParamList, body: BlockStmt) -> None:
        super().__init__(Decl.Type.Func)
        self.params = params
        self.body = body


class FuncDecl(AbstractFuncDecl):
    def __init__(self, name: Token, params: ParamList, body: BlockStmt) -> None:
        super().__init__(params, body)
        self.name = name


    def accept(self, visitor: DeclVisitor[T]) -> T:
        return visitor.visit_func(self)
