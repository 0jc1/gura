from expr import Visitor, Expr
from tokens import TokenType, Token

class Interpreter(Visitor):

    def __init__(self):
        pass

    def visitLiteralExpr(self, expr : Expr):
        return expr.value 

    def visitGroupExpr(self, expr : Expr):
        return self.eval(expr.expression)

    def visitUnaryExpr(self, expr):
        right = self.eval(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return ~self.isTruthy(right)

        # unreachable 
        return None 
    
    def visitBinaryExpr(self, expr):
        left = self.eval(expr.left)
        right = self.eval(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.PLUS:
                if (type(left) == float and type(right) == float):
                    return float(left) + float(right)
                if (type(left) == str and type(right) == str):
                    return str(left) + str(right)
                break 
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)   
            case TokenType.BANG_EQUAL:
                return ~self.isEqual(left, right)
            case TokenType.BANG:
                return self.isEqual(left,right)
            
        return None  

    def isEqual(self, a, b):
        if ( a is None ) and (b is None):
            return True
        if (a is None):
            return False
        return a == b

    def isTruthy(self, obj):
        if obj is None:
            return False 
        if type(obj) == bool:
            return bool(obj)
        return True 

    def eval(self, expr):
        return expr.accept(self)


