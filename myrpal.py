from Lexer.lexicalAnalyzer import tokenize
from Parser.parser import ASTParser
from Standardizer.standardizer import Standardizer
from Standardizer.st_node import STNode
from cse_machine.rules import CSEMachine
from cse_machine.cse_machine import CSEMachineFactory
import sys
import argparse

if __name__ == "__main__":

    # # Check if a file path is provided as a command-line argument
    # if len(sys.argv) > 1:
    #     input_file = sys.argv[1]
    # else:
    #     # Default file if no argument is provided
    #     input_file = "E:/PLProject/RPAL-parser/Inputs/Q1.txt"
    parser = argparse.ArgumentParser(description='Process some RPAL files.')
    parser.add_argument('file_name', type=str, help='The RPAL program input file')
    parser.add_argument('-ast', action='store_true', help='Print the abstract syntax tree')
    parser.add_argument('-st', action='store_true', help='Print the standardized abstract syntax tree')

    args = parser.parse_args()

    input_file = open(args.file_name, "r")
     
    input_text = input_file.read()
    input_file.close()
    
    # Tokenize the input text
    tokens = tokenize(input_text)
    try:
        

        parser = ASTParser(tokens=tokens)
        parse_tree = parser.parse()
        if args.ast:
            print("\n🌳 Abstract Syntax Tree:")
            parse_tree.print_tree()
        
        
        standardizer = Standardizer()
        standard_tree = standardizer.standardize(parse_tree)
        if args.st:
            print("\n🌲 Standardized  Tree:")
            standard_tree.print()
        
        

        # print("\n root value is...", str(standard_tree.get_data()))
        # print(isinstance(standard_tree, STNode))

        print("\n CSE Machine starts\n")

        cse_machine_factory = CSEMachineFactory()
        cse_machine = cse_machine_factory.get_cse_machine(standard_tree)

        print("\nOutput of the above program is:")
        print(cse_machine.get_answer())
        
        # print("\nPrint the stack:")
        # print(cse_machine.print_stack())

        
    
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        sys.exit(1)       


        