from tokens import Token, TokenType
from gura import error
class Scanner():
    tokens : list[Token] = []
    start = 0
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
        for char in self.source:
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()
        match c:
            case '(': self.addToken(TokenType.LEFT_PAREN); return
            case ')': self.addToken(TokenType.RIGHT_PAREN); return
            case '{': self.addToken(TokenType.LEFT_BRACE); return
            case '}': self.addToken(TokenType.RIGHT_BRACE); return
            case ',': self.addToken(TokenType.COMMA); return
            case '.': self.addToken(TokenType.DOT); return
            case '-': self.addToken(TokenType.MINUS); return
            case '+': self.addToken(TokenType.PLUS); return
            case ';': self.addToken(TokenType.SEMICOLON); return
            case '*': self.addToken(TokenType.STAR); return

            case '=': self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL); return
            case '<': self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS); return
            case '>': self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER); return
            case '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG); return

            case '/':
                while self.peek() != '\n' and not self.atEnd(): self.advance() if self.match('/') else self.addToken(TokenType.SLASH)

            #whitespace
            case ' ': return
            case '\r': return
            case '\t': return

            # new line
            case '\n':
                self.line += 1
                return

            #literals
            case '"': self.string(); return

            case 'o':
                if self.match('r'):
                    self.addToken(TokenType.OR)



            case default:
                if c.isdigit():
                    self.number()
                else:
                    error(self.line, 'Unexpected character')
                return

    def number(self):
        start = self.current
        while (self.peek().isdigit()): self.advance()

        if (self.peek() == '.' and self.peek(1).isdigit()): # consume the "."
            self.advance()

        while (self.peek().isdigit()): self.advance()

        val = self.source[start : self.current]
        self.addToken(TokenType.NUMBER, float(val))


    def string(self):
        start = self.current
        while (self.peek() != '"' and not self.atEnd()):
            if self.peek() == '\n':
                self.line +=1
            self.advance()
        if self.atEnd():
            error(self.line, "unterminated string")

        val = self.source[start+1 : self.current-1]
        self.addToken(TokenType.STRING, val)

    def identifier(self):
        start = self.current
        while self.peek().isalnum(): self.advance()

        text = self.source[start:self.current]
        t = self.keywords.get(text)

        if t==None:
            t = TokenType.IDENTIFIER
        self.addToken(t)


    def peek(self, offset=0):
        if self.atEnd(): return '\0'
        return self.source[self.current + offset]

    def atEnd(self):
        return len(self.source) <= self.current + 1

    def match(self, expected):
        if self.atEnd(): return False
        if self.source[self.current] != expected: return False
        current += 1
        return True

    def advance(self):
        c = self.source[current]
        current += 1
        return c

    def addToken(self, token, literal=None):
        self.tokens.append(Token(token, literal, self.line))


