import enum

class TokenKind(enum.Enum):
    Invalid = 0
    Number = 1
    Identifier = 2

    Kw_var = 12
    Kw_const = 13

    Op_Plus = 23
    Op_Minus = 24
    Op_Star = 25
    Op_Slash = 26
    Op_LParen = 27
    Op_RParen = 28
    Op_Equal = 29
    Op_EqualEqual = 30
    Op_Exclaim = 31
    Op_ExclaimEqual = 32

    End = 100