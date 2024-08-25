from expr import Expr, Visitor

class AstPrinter(Visitor):
    def print(self, expr):
        if expr is None:
            return
        return expr.accept(self)

    def visitBinary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr):
        if expr.value == None: return "null"
        return str(expr.value)

    def visitUnary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *args):
        result = "(" + name
        for expr in args:
            result = result + " "
            result = result + expr.accept(self)
        result = result + ")"
        return result