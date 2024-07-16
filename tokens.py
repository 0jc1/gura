from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    OR = auto()
    AND = auto()
    FUN = auto()
    CLASS = auto()
    NULL = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    VAR = auto()
    RETURN = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    BANG_EQUAL = auto()
    BANG = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    DOT = auto()

    # Delimiters
    SEMICOLON = auto()
    COMMA = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # End of file
    EOF = auto()

class Token():
    def __init__(self, ttype : TokenType, lexeme, literal, line ):
        self.type = ttype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

