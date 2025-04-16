from Lexer.lexicalAnalyzer import tokenize
from Parser.parser import ParseNode

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

    print("\n🌲 Parsing the Tokens:")
    # Initialize the parser with the tokens
    parser = ParseNode(tokens)
    try:
        # Parse the tokens and generate the parse tree
        parse_tree = parser.parse()
        print("\n✅ Parse Tree:")
        print(parse_tree)  
    except SyntaxError as e:
        print(f"\n❌ Syntax Error: {e}")