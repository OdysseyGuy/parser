from lex.tokenkind import TokenKind


KEYWORDS: 'list[tuple[str, TokenKind]]' = [
    ('var',     TokenKind.Kw_var),
    ('const',   TokenKind.Kw_const),
]


def is_keyword(token: str) -> bool:
    for keyword in KEYWORDS:
        if token == keyword[0]:
            return True
    return False


def ident_to_keyword(token: str) -> TokenKind:
    for keyword in KEYWORDS:
        if token == keyword[0]:
            return keyword[1]
    return TokenKind.Invalid
