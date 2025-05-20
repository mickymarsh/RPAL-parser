from Lexer.lexicalAnalyzer import tokenize
from Parser.parser import ASTParser

if __name__ == "__main__":
    # Read code from the file inside "input" folder
    with open("E:/PLProject/RPAL-parser/Inputs/Q1.txt", "r") as file:


        code = file.read()
    print("🔍 Input code:")
    print(code)

    print("\n🧪 Lexical Analysis (Tokens):")

    tokens = tokenize(code)
    print("\n✅ Final Tokens:")
    for token in tokens:


        print(f"Type: {token.getType().name}, Value: {token.getContext()}")

    # Create a parser instance with the tokens


    parser = ASTParser(tokens=tokens)
    # Parse the tokens into a syntax tree
    parse_tree = parser.parse()
    # Print the parse tree using the class method
    print("\n🌳 Parse Tree:")
    parse_tree.print_tree()