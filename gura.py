import sys
from scanner import Scanner

hadError = False

def error(line: int, msg: str):
    report(line, "", msg)

def report(line: int, where: str, msg: str):
    print(f"[{line}] error {where} : {msg}")
    hadError = True

def run(source):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    print([vars(instance) for instance in tokens])
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
        run(content)

        if hadError:
            sys.exit(65)
    except FileNotFoundError:
        return f"Error: The file '{filename}' was not found."
    except IOError:
        return f"Error: An error occurred while reading the file '{filename}'."

def main(args):
    if len(args) > 2:
        print("Usage: python3 gura.py <script>")
    elif len(args) == 2:
        runFile(args[1])
    else:
        print("Gura 0.0.0")
        runPrompt()

if __name__ == "__main__":
    main(sys.argv)