from core.tokenkind import TokenKind


KEYWORDS: dict[str, TokenKind] = {
    'let':          TokenKind.Kw_let,
    'func':         TokenKind.Kw_func,
    'and':          TokenKind.Kw_and,
    'or':           TokenKind.Kw_or,
    'not':          TokenKind.Kw_not,
    'if':           TokenKind.Kw_if,
    'else':         TokenKind.Kw_else,
    'while':        TokenKind.Kw_while,
    'return':       TokenKind.Kw_return,
    'class':        TokenKind.Kw_class,
    'interface':    TokenKind.Kw_interface,
    'self':         TokenKind.Kw_self,
}
