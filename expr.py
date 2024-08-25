from abc import ABC, abstractmethod

from tokens import Token

# base classes
class Expr:
    @abstractmethod
    def accept():
        raise NotImplementedError("Subclasses must implement this method")

class Visitor:
    def visit():
        pass

# AST classes
class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinary(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGrouping(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)