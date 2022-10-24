from typing import Generic, Optional, TypeVar


T = TypeVar("T")

class ParserResult(Generic[T]):
    """Wrapper around statments, expressions and declarations with
    an additional `iserror` value which stores if there is an error
    in the parse tree.
    """
    def __init__(self, iserror: bool, data: Optional[T]) -> None:
        self.data = data
        self.iserror = iserror
