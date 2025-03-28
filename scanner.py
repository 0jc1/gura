from tokens import Token, TokenType
from logger import *

class Scanner():
    tokens = []
    start = 0
    source = ""
    tokenStart = 0
    current = 0
    line = 1
    keywords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "or": TokenType.OR,
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "fun": TokenType.FUN,
        "null": TokenType.NULL,
        "print": TokenType.PRINT,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "var": TokenType.VAR,
        "return": TokenType.RETURN
    }

    def __init__(self, source):
        self.source = source

    def scanTokens(self):
        while not self.atEnd():
            self.start = self.current
            self.scanToken()

        self.tokenStart = self.current
        self.addToken(TokenType.EOF)
        return self.tokens

    def scanToken(self):
        c = self.advance()
        self.tokenStart = self.current
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
            return
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
            return
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
            return
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
            return
        elif c == ',':
            self.addToken(TokenType.COMMA)
            return
        elif c == '.':
            self.addToken(TokenType.DOT)
            return
        elif c == '-':
            self.addToken(TokenType.MINUS)
            return
        elif c == '+':
            self.addToken(TokenType.PLUS)
            return
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
            return
        elif c == '*':
            self.addToken(TokenType.STAR)
            return

        elif c == '=':
            self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            return
        elif c == '<':
            self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            return
        elif c == '>':
            self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            return
        elif c == '!':
            self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            return

        elif c == '/':
            if self.peek(1) == '/':
                while self.peek() != '\n' and not self.atEnd():
                    self.advance()
            elif self.peek(1) == '*':
                while not self.matchStr('*/') and not self.atEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)

        # whitespace
        elif c == ' ':
            return
        elif c == '\r':
            return
        elif c == '\t':
            return

        # new line
        elif c == '\n':
            self.line += 1
            return

        # literals
        elif c == '"':
            self.string()
            return

        else:
            if c.isdigit():
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                error(self.line, 'Unexpected character ' + c)
            return

    def number(self):
        start = self.current
        while (self.peek().isdigit()): self.advance()

        if (self.peek() == '.' and self.peek(1).isdigit()): # consume the "."
            self.advance()

        while (self.peek().isdigit()): self.advance()

        val = self.source[start-1 : self.current]
        if '.' in val:
            self.addToken(TokenType.NUMBER, float(val))
        else:
            self.addToken(TokenType.NUMBER, int(val))


    def string(self):
        start = self.current
        while self.peek() != '"' and not self.atEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.atEnd():
            error(self.line, "Unterminated string")

        literal = self.source[start : self.current]
        self.advance()
        self.addToken(TokenType.STRING, literal)

    def identifier(self):
        start = self.current
        while self.peek().isalnum(): self.advance()

        text = self.source[start-1 : self.current]
        t = self.keywords.get(text)

        if t==None:
            t = TokenType.IDENTIFIER
        self.addToken(t)

    def peek(self, offset=0):
        if self.atEnd(): return '\0'
        return self.source[self.current + offset]

    def atEnd(self):
        return len(self.source) <= self.current

    def matchStr(self, expected):
        for c in expected:
            if not self.match(c): return False
        return True

    def match(self, expected):
        if self.atEnd(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, token, literal=None):
        lexeme = self.source[self.tokenStart-1 : self.current]
        self.tokens.append(Token(token, lexeme, literal, self.line))
        # print(f"token added {token} {lexeme} {literal}")


