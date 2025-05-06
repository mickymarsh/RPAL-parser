from Lexer.lexicalAnalyzer import tokenize
from Parser.grammar import Parser

if __name__ == "__main__":
    # Read code from the file inside "input" folder
    with open("Inputs/Q1.txt", "r") as file:
        code = file.read()

    print("Input code:")
    print(code)

    tokens = tokenize(code)
    print("\nLexical Analysis (Tokens):")
    for token in tokens:
        print(f"Type: {token.getType().name}, Context: {token.getContext()}")

    print("Lexical analyzer finished")

    parser = Parser(tokens=tokens)
    parser.parse()