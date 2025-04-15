from Lexer.lexicalAnalyzer import tokenize

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