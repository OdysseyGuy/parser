from asttypes.expr import Expr


class ParamList(list[Expr]):
    def __init__(self, params: list[Expr]):
        self.params = params
