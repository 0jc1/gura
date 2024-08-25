import sys
from tokens import *
from scanner import Scanner
from expr import *
from astprinter import AstPrinter
from logger import *
from parser import Parser


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    # print([vars(instance) for instance in tokens])

    parser = Parser(tokens)
    expression = parser.parse()

    if hadError:
        return
    
    print(AstPrinter().print(expression))
    pass

def runPrompt():
    while True:
        print("> ", end="")
        line = input()
        if line == "": continue
        run(line)
        hadError = False

def runFile(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        if content == "": return
        run(content)

        if hadError:
            sys.exit(65)
    except FileNotFoundError:
        return f"Error: The file '{filename}' was not found."
    except IOError:
        return f"Error: An error occurred while reading the file '{filename}'."

def main(args):

    # expression = Binary(
    #     Unary(
    #         Token(TokenType.MINUS, "-", None, 1),
    #         Literal(111)),
    #     Token(TokenType.STAR, "*", None, 1),
    #     Grouping(Literal(45.3))
    #             )

    # print(AstPrinter().print(expression))

    if len(args) > 2:
        print("Usage: python3 gura.py <script>")
    elif len(args) == 2:
        runFile(args[1])
    else:
        print("Gura v0.0.0")
        runPrompt()

if __name__ == "__main__":
    main(sys.argv)