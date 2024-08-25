from tokens import *

hadError = False

def error(line: int, msg: str):
    report(line, "", msg)
    raise Exception()

def report(line: int, where: str, msg: str):
    print(f"[{line}] error {where} : {msg}")
    hadError = True 

def error2(token : Token, msg: str):
    if token.type == TokenType.EOF:
        report(token.line, "at end", msg)
    else:
        report(token.line, "at '" + token.lexeme + "'", msg)
    raise Exception()