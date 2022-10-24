import enum


class TokenKind(enum.Enum):
    Invalid         = enum.auto()
    End             = enum.auto()
    Number          = enum.auto()
    Identifier      = enum.auto()

    # -------- Operators --------
    Op_Plus         = enum.auto()
    Op_Minus        = enum.auto()
    Op_Star         = enum.auto()
    Op_Slash        = enum.auto()
    Op_LBrace       = enum.auto()
    Op_RBrace       = enum.auto()
    Op_LParen       = enum.auto()
    Op_RParen       = enum.auto()
    Op_Equal        = enum.auto()
    Op_EqualEqual   = enum.auto()
    Op_Exclaim      = enum.auto()
    Op_ExclaimEqual = enum.auto()
    Op_Greater      = enum.auto()
    Op_GreaterEqual = enum.auto()
    Op_Less         = enum.auto()
    Op_LessEqual    = enum.auto()
    Op_Comma        = enum.auto()
    Op_Colon        = enum.auto()

    # -------- Keywords --------
    Kw_let          = enum.auto()
    Kw_func         = enum.auto()
    Kw_const        = enum.auto()
    Kw_and          = enum.auto()
    Kw_or           = enum.auto()
    Kw_not          = enum.auto()
    Kw_if           = enum.auto()
    Kw_else         = enum.auto()
    Kw_while        = enum.auto()
    Kw_return       = enum.auto()
    Kw_class        = enum.auto()
    Kw_interface    = enum.auto()
    Kw_self         = enum.auto()
