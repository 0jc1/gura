from tokens import Token, TokenType
from expr import *
from typing import List
from logger import * 


"""
Expression grammar:

expr -> equality
equality -> comparison (( != | == ) comparison)*
comparison -> term  ( ( > | >= | < | <= ) term)*
factor -> unary ( ( / | * ) unary )*
unary -> ( ! | - ) unary | primary
primary -> NUMBER | STRING | true | false | null | "(" expr ")"

"""

class Parser():
    tokens : List[Token] = [] 
    current = 0

    def __init__(self, tokens : List[Token]):
        self.tokens = tokens

    def parse(self) -> Expr:
        try:
            return self.expression()
        except:
            return None

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, t):    
        if self.isAtEnd(): return False
        return self.peek().type == t

    def advance(self) -> Token:
        if not self.isAtEnd(): 
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr = self.comparison()
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator : Token = self.previous()
            right : Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expr:
        expr = self.factor()
        while(self.match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr 
    
    def factor(self) -> Expr:   
        expr = self.unary()
        while(self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr:
        if (self.match(TokenType.BANG, TokenType.MINUS)):
            operator = self.previous()
            right = self.unary()
            expr = Unary(operator, right)
            return expr 
        return self.primary()

    def primary(self) -> Expr:
        if (self.match(TokenType.FALSE)): return Literal(False)
        if (self.match(TokenType.TRUE)): return Literal(True)
        if (self.match(TokenType.NULL)): return Literal(None)

        if (self.match(TokenType.NUMBER, TokenType.STRING)):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr) 
        
        error2(self.peek(), "Expect expression.")

    def consume(self, ttype, msg) -> Token:
        if self.check(ttype):
            return self.advance()
        else:
            error2(self.peek(), msg)

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON: 
                return
            match self.peek().type:
                case TokenType.CLASS: 
                    return
                case TokenType.FOR:
                    return
                case TokenType.FUN:
                    return
                case TokenType.IF:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.WHILE:
                    return    
            self.advance()