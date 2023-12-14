# Parser
Simple lexer and parser written in Python that uses Recursive Descent Parser to parse grammar rules.

# Grammar
The parser lists the following grammar.

## Expressions
```
expression      -> assignment
assingment      -> IDENTIFIER "=" assignment | logicalOr
logicalOr       -> logicalAnd ("or" logicalAnd)*
logicalAnd      -> equality ("and" equality)*
equality        -> comparison (("==" | "!=") comparison)*
comparison      -> term (("<" | "<=" | ">" | ">=") term)*
term            -> factor (("+" | "-") factor)*
factor          -> unary (("/" | "*") unary)*
unary           -> ("-") unary | call
call            -> primary ("(" arguments? ")")+
arguments       -> expression ("," expression)*
primary         -> LITERAL | IDENTIFIER | "(" expression ")"
```

## Statements and Declarations
```
program         -> decl End
decl            -> letDecl | funcDecl | stmt
stmt            -> exprStmt | ifStmt | whileStmt | returnStmt | block
brace           -> "{" decl* "}"

letDecl         -> "let" IDENTIFIER ("=" expression)?
funcDecl        -> "func" IDENTIFIER "=" "(" parameters? ")" block
parameters      -> IDENTIFIER ("," IDENTIFIER)*
classDecl       -> "class" IDENTIFIER "{" decl* "}"

ifStmt          -> "if" "(" expression ")" stmt
                   ("else" stmt)?
whileStmt       -> "while" "(" expression ")" stmt
returnStmt      -> "return" expression? ("if" expresssion)?
```
