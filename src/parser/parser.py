"""Contains the parser implementation."""

from __future__ import annotations
from asttypes.astnode import ASTNode

from asttypes.expr import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    Expr,
    GroupExpr,
    InvalidExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr
)
from asttypes.paramlist import ParamList
from asttypes.stmt import (
    BlockStmt,
    IfStmt,
    ReturnStmt,
    Stmt,
    ExprStmt,
    WhileStmt
)
from asttypes.decl import (
    ClassDecl,
    Decl,
    FuncDecl,
    InvalidDecl,
    LetDecl
)

from core.ops import BinaryOp, UnaryOp, token_to_binaryop, token_to_unaryop
from core.tokenkind import TokenKind

from lexer.token import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        """Creates a parser object.

        Args:
            tokens: List of tokens from the lexer.
        """
        self.tokens: list[Token] = tokens
        self.current: int = 0

    def peek(self) -> Token:
        """Returns the current token before it is consumed."""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Returns the previously consumed token."""
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().is_kind(TokenKind.End)

    def consume(self) -> Token:
        """Advances to the next token in the list. Returns the currently
        consumed token.
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def must_consume(self, kind: TokenKind, message: str):
        """Consume the given kind of token and if current token is not of
        that kind then raise an error exception.
        """
        if self.check(kind):
            return self.consume()
        else:
            raise Exception(message)

    def check(self, kind: TokenKind) -> bool:
        """Check if current token is of specified kind."""
        return self.peek().is_kind(kind)

    def match(self, *kinds: TokenKind) -> bool:
        """Checks if current token is of specified kind. If it is
        then it consumes the token and returns true else returns false.

        Use `previous()` method to get the consumed token.
        """
        if self.peek().is_any(*kinds):
            self.consume()
            return True
        return False

    # ------------------------------ Expressions ------------------------------
    def parse_expr(self) -> Expr:
        return self.parse_assignment_expr()

    def parse_assignment_expr(self) -> Expr:
        expr = self.parse_logical_or()

        if self.match(TokenKind.Op_Equal):
            # TODO: Implement assignment
            value: Expr = self.parse_assignment_expr()

            # Check if the left hand expression is a valid l-value
            # i.e., left hand should be a variable expression
            if isinstance(expr, VariableExpr):
                name: Token = expr.name
                return AssignExpr(name, value)
            else:
                raise Exception("Invalid assignment expression.")

        return expr

    def parse_logical_or(self) -> Expr:
        expr = self.parse_logical_and()

        while self.match(TokenKind.Kw_or):
            right: Expr = self.parse_logical_and()
            expr = BinaryExpr(expr, BinaryOp.Or, right)

        return expr

    def parse_logical_and(self) -> Expr:
        expr = self.parse_equality_expr()

        while self.match(TokenKind.Kw_and):
            right: Expr = self.parse_equality_expr()
            expr = BinaryExpr(expr, BinaryOp.And, right)

        return expr

    def parse_equality_expr(self) -> Expr:
        expr = self.parse_comparison_expr()

        while self.match(TokenKind.Op_EqualEqual, TokenKind.Op_ExclaimEqual):
            op: BinaryOp = token_to_binaryop(self.previous())
            right: Expr = self.parse_comparison_expr()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_comparison_expr(self) -> Expr:
        expr = self.parse_term_expr()

        while self.match(TokenKind.Op_Less, TokenKind.Op_LessEqual,
            TokenKind.Op_Greater, TokenKind.Op_GreaterEqual):
            op: BinaryOp = token_to_binaryop(self.previous())
            right: Expr = self.parse_term_expr()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_term_expr(self) -> Expr:
        expr = self.parse_factor_expr()

        while self.match(TokenKind.Op_Plus, TokenKind.Op_Minus):
            op: BinaryOp = token_to_binaryop(self.previous())
            right: Expr = self.parse_factor_expr()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_factor_expr(self) -> Expr:
        expr = self.parse_unary_expr()

        while self.match(TokenKind.Op_Slash, TokenKind.Op_Star):
            op: BinaryOp = token_to_binaryop(self.previous())
            right: Expr = self.parse_unary_expr()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_unary_expr(self) -> Expr:
        if self.match(TokenKind.Op_Minus, TokenKind.Op_Exclaim):
            op: UnaryOp = token_to_unaryop(self.previous())
            expr: Expr = self.parse_unary_expr()
            return UnaryExpr(op, expr)

        return self.parse_call_expr()

    def parse_call_expr(self) -> Expr:
        expr = self.parse_primary_expr()

        # TODO: Check if the parenthesis even has any arguments before
        #       trying to parse any arguments.
        while self.match(TokenKind.Op_LParen):
            args: list[Expr] = self.parse_call_expr_args()
            self.must_consume(TokenKind.Op_RParen, "Expected ')' after arguments.")
            expr = CallExpr(expr, args)

        return expr

    def parse_call_expr_args(self) -> list[Expr]:
        args: list[Expr] = []

        if not self.check(TokenKind.Op_RParen):
            args.append(self.parse_expr())
            while self.match(TokenKind.Op_Comma):
                args.append(self.parse_expr())

        return args

    def parse_primary_expr(self) -> Expr:
        if self.match(TokenKind.Number):
            return LiteralExpr(self.previous().get_literal_data()) # type: ignore

        if self.match(TokenKind.Op_LParen):
            expr: Expr = self.parse_expr()
            self.must_consume(TokenKind.Op_RParen, "Expected ')' after expression.")
            return GroupExpr(expr)

        if self.match(TokenKind.Identifier):
            return VariableExpr(self.previous())

        return InvalidExpr()

    # ------------------------------ Declarations ------------------------------
    def parse_decl(self) -> Decl:
        if self.match(TokenKind.Kw_let):
            return self.parse_let_decl()

        if self.match(TokenKind.Kw_func):
            return self.parse_func_decl()

        if self.match(TokenKind.Kw_class):
            return self.parse_class_decl()

        return InvalidDecl()

    def parse_let_decl(self) -> Decl:
        name: Token = self.must_consume(TokenKind.Identifier, "Expected an identifier.")

        initializer: Expr | None = None
        if self.match(TokenKind.Op_Equal):
            initializer = self.parse_expr()

        return LetDecl(name, initializer)

    def parse_func_decl(self) -> Decl:
        # TODO: Should be force require brace statement as the function body?
        name: Token = self.must_consume(TokenKind.Identifier, "Expected an identifier.")

        self.must_consume(TokenKind.Op_LParen, "Expected '(' after function name.")
        params: ParamList = self.parse_func_parameters()
        self.must_consume(TokenKind.Op_RParen, "Expected ')' after parameter.")

        self.must_consume(TokenKind.Op_LBrace, "Expected a '{' before function body.")
        body: Stmt = self.parse_block_stmt()

        return FuncDecl(name, params, body)

    def parse_func_parameters(self) -> ParamList:
        args: ParamList = ParamList([])

        if not self.check(TokenKind.Op_RParen):
            args.append(self.parse_expr())
            while self.match(TokenKind.Op_Comma):
                args.append(self.parse_expr())

        return args

    def parse_class_decl(self) -> ClassDecl:
        name: Token = self.must_consume(TokenKind.Identifier, "Expected an identifier as class name.")

        # Inheritance list?
        inheritance_list: list[Token] = []
        if self.check(TokenKind.Op_Colon):
            self.consume()
            inheritance_list = self.parse_inheritance_list()

        self.must_consume(TokenKind.Op_LBrace, "Expected '{' before class body.")
        block_stmt: BlockStmt = self.parse_block_stmt()

        return ClassDecl(name, inheritance_list)

    def parse_inheritance_list(self) -> list[Token]:
        inherited: list[Token] = []
        inherited.append(self.must_consume(TokenKind.Identifier, ""))

        return inherited

    # ------------------------------ Statements ------------------------------
    def parse_stmt(self) -> Stmt:
        """statement:
            block-statement |
            if-statement |
            while-statement;
        """
        if self.match(TokenKind.Op_LBrace):
            return self.parse_block_stmt()

        if self.match(TokenKind.Kw_if):
            return self.parse_if_stmt()

        if self.match(TokenKind.Kw_while):
            return self.parse_while_stmt()

        if self.match(TokenKind.Kw_return):
            return self.parse_return_stmt()

        return self.parse_expr_stmt()

    def parse_if_stmt(self) -> IfStmt:
        """if-statement:
            'if' '(' expression ')' block
            'else' block
        """
        # TODO: Implement if-else-if-else
        self.must_consume(TokenKind.Op_LParen, "Expected '(' after 'if'.")
        condition: Expr = self.parse_expr()
        self.must_consume(TokenKind.Op_RParen, "Expected ')' after if condition.")

        # handle dangling else by requiring a brace for the if body
        # if not self.check(TokenKind.Op_LBrace):
        #     raise Exception("Expected '{' after if condition.")

        thenbranch: Stmt = self.parse_stmt()

        # keep looking for else (greedy) if we can't find one we will return
        elsebranch: Stmt | None = None
        if self.match(TokenKind.Kw_else):
            elsebranch = self.parse_stmt()

        return IfStmt(condition, thenbranch, elsebranch)

    def parse_while_stmt(self) -> WhileStmt:
        """while-statement:
            'while' '(' expression ')' block
        """
        # parse condition
        self.must_consume(TokenKind.Op_LParen, "Expected '(' after 'while'.")
        condition: Expr = self.parse_expr()
        self.must_consume(TokenKind.Op_RParen, "Expected ')' after while condition.")

        # parse body
        body: Stmt = self.parse_stmt()
        return WhileStmt(condition, body)

    def parse_return_stmt(self) -> ReturnStmt:
        # TODO: Check if there is an expression
        expr: Expr = self.parse_expr()
        return ReturnStmt(expr, None)

    def parse_block_stmt(self) -> BlockStmt:
        elems: list[ASTNode] = []

        while not self.check(TokenKind.Op_RBrace) and not self.is_at_end():
            decl: ASTNode = self.parse_decl()
            elems.append(decl)

        self.must_consume(TokenKind.Op_RBrace, "Expected '}' after block.")
        return BlockStmt(elems)

    def parse_expr_stmt(self):
        expr = self.parse_expr()
        return ExprStmt(expr)

    def parse(self):
        stmts: list[Decl] = []
        while not self.is_at_end():
            stmts.append(self.parse_decl())

        try:
            return self.parse_expr()
        except Exception as e:
            print(f"Error: {str(e)}")
