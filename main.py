from Lexer.lexicalAnalyzer import tokenize
from Parser.parser import ASTParser
from Standardizer.standardizer import Standardizer
from Standardizer.st_node import STNode
from cse_machine.rules import CSEMachine
from cse_machine.cse_machine import CSEMachineFactory

if __name__ == "__main__":
    # Read code from the file inside "input" folder
    with open("Inputs\sir.txt", "r") as file:


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

    print("\n root value is...", str(standard_tree.get_data()))

    print(isinstance(standard_tree, STNode))

    print("\n CSE Machine starts\n")

    cse_machine_factory = CSEMachineFactory()
    cse_machine = cse_machine_factory.get_cse_machine(standard_tree)

    print("\nOutput of the above program is:")
    print(cse_machine.get_answer())
    



    