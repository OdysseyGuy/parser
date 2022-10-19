import enum
from lexer.token import Token
from core.tokenkind import TokenKind


class BinaryOp(enum.Enum):
    Invalid     = enum.auto()

    Add         = enum.auto()
    Sub         = enum.auto()
    Mul         = enum.auto()
    Div         = enum.auto()

    Less        = enum.auto()
    Greater     = enum.auto()
    LessEq      = enum.auto()
    GreaterEq   = enum.auto()

    EqEq        = enum.auto()
    NotEq       = enum.auto()

    And         = enum.auto()
    Or          = enum.auto()
    Xor         = enum.auto()


class UnaryOp(enum.Enum):
    Invalid     = enum.auto()
    Negate      = enum.auto()
    Not         = enum.auto()


def token_to_binaryop(token: Token) -> BinaryOp:
    if token.is_kind(TokenKind.Op_Plus):
        return BinaryOp.Add
    elif token.is_kind(TokenKind.Op_Minus):
        return BinaryOp.Sub
    elif token.is_kind(TokenKind.Op_Star):
        return BinaryOp.Mul
    elif token.is_kind(TokenKind.Op_Slash):
        return BinaryOp.Div
    elif token.is_kind(TokenKind.Op_Less):
        return BinaryOp.Less
    elif token.is_kind(TokenKind.Op_Greater):
        return BinaryOp.Greater
    elif token.is_kind(TokenKind.Op_LessEqual):
        return BinaryOp.LessEq
    elif token.is_kind(TokenKind.Op_GreaterEqual):
        return BinaryOp.GreaterEq
    elif token.is_kind(TokenKind.Op_EqualEqual):
        return BinaryOp.EqEq
    elif token.is_kind(TokenKind.Op_ExclaimEqual):
        return BinaryOp.NotEq
    else:
        return BinaryOp.Invalid


def token_to_unaryop(token: Token) -> UnaryOp:
    if token.is_kind(TokenKind.Op_Minus):
        return UnaryOp.Negate
    elif token.is_kind(TokenKind.Op_Exclaim):
        return UnaryOp.Not
    else:
        return UnaryOp.Invalid
