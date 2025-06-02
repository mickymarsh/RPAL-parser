from Lexer.lexicalAnalyzer import tokenize
from Parser.parser import ASTParser
from Standardizer.standardizer import Standardizer

if __name__ == "__main__":
    # Read code from the file inside "input" folder
    with open("Inputs/Q1.txt", "r") as file:


        code = file.read()
    print("🔍 Input code:")
    print(code)

    print("\n🧪 Lexical Analysis (Tokens):")

    tokens = tokenize(code)
    print("\n✅ Final Tokens:")
    for token in tokens:
        print(f"Type: {token.getType().name}, Value: {token.getContext()}")

    parser = ASTParser(tokens=tokens)
    parse_tree = parser.parse()
    print("\n🌳 Abstract Syntax Tree:")
    parse_tree.print_tree()
    print("\n🌳 Abstract Syntax Tree as String:")
    parse_tree.print_tree_as_string()

    
    standardizer = Standardizer()
    standard_tree = standardizer.standardize(parse_tree)

    print("\n🌲 Standardized Tree (ST):")
    standard_tree.print()