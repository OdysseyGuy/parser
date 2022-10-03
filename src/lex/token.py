from lex.tokenkind import TokenKind
from lex.keywords import is_keyword


class Token:
    def __init__(self, kind: TokenKind) -> None:
        self.kind = kind
        self.data = ''


    def set_data(self, data: str) -> None:
        self.data: str = data


    def get_literal_data(self) -> str:
        return self.data


    def is_of_kind(self, tok_kind: TokenKind) -> bool:
        return self.kind == tok_kind


    def is_keyword(self) -> bool:
        return is_keyword(self.kind)


    def __str__(self) -> str:
        s = 'kind: ' + str(self.kind)

        if self.data != '':
            s += ', data: ' + self.data

        return s
