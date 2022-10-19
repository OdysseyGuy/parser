from core.tokenkind import TokenKind


KEYWORDS: dict[str, TokenKind] = {
    'let':      TokenKind.Kw_let,
    'and':      TokenKind.Kw_and,
    'or':       TokenKind.Kw_or,
    'not':      TokenKind.Kw_not,
    'if':       TokenKind.Kw_if,
    'else':     TokenKind.Kw_else,
    'while':    TokenKind.Kw_while,
    'func':     TokenKind.Kw_func
}
