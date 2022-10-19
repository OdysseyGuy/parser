from core.tokenkind import TokenKind


class Token:
    def __init__(self, kind: TokenKind) -> None:
        self.__kind = kind
        self.__data: str | None = None


    def is_identifier(self) -> bool:
        return self.is_kind(TokenKind.Identifier)


    def is_literal(self) -> bool:
        return self.is_kind(TokenKind.Number)


    def set_literal_data(self, data: str) -> None:
        assert self.is_literal(), "Cannot set literal data for non-literal!"
        self.__data = data


    def set_identifier_data(self, data: str) -> None:
        assert self.is_identifier(), "Cannot set identifier data for non-identifier!"
        self.__data = data


    def get_literal_data(self) -> str | None:
        assert self.is_literal(), "Cannot get literal data for non-literal!"
        return self.__data


    def get_identifier_data(self) -> str | None:
        if self.is_literal():
            return None
        return self.__data


    def is_kind(self, tok_kind: TokenKind) -> bool:
        return self.__kind == tok_kind


    def is_any(self, *kinds: TokenKind) -> bool:
        for kind in kinds:
            if self.__kind == kind:
                return True
        return False

    def is_keyword(self) -> bool:
        # TODO: Implement keyword dictionary lookup
        return False


    def __str__(self) -> str:
        s = 'kind: ' + str(self.__kind)
        if self.__data != None:
            s += ', data: ' + self.__data
        return s
