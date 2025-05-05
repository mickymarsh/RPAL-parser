from build_ast import TreeBuilder
from node import Node  
from Lexer.validTokens import validTokenTypes, validToken

class Parser:
    def __init__(self, tokens: list[validToken]):
        self.tokens = tokens
        self.builder = TreeBuilder()

    def parse(self):
        self.tokens.append(validToken(validTokenTypes.End_of_tokens, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        if self.tokens[0].type == validTokenTypes.End_of_tokens:
            return self.builder.stack
        else:
            print("Parsing Unsuccessful!...........")
            
"""
    # Expressions 
                
    # E	->'let' D 'in' E		=> 'let'
    # 	->'fn' Vb+ '.' E		=> 'lambda'
    # 	->Ew;

    def E(self):
        if self.tokens:  # Ensure tokens list is not empty
            token = self.tokens[0]
            if hasattr(token, 'type') and hasattr(token, 'value'):  # Check if token has type and value attributes
                if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
                    # print('Entering if block in E...')
                    if token.value == "let":
                        # print('Entering let block...')
                        self.tokens.pop(0)  # Remove "let"
                        self.D()
                        if self.tokens[0].value != "in":
                            print("Parse error at E : 'in' Expected")
                        self.tokens.pop(0)  # Remove "in"
                        self.E()
                        self.ast.append(Node(NodeType.let, "let", 2))
                    else:
                        self.tokens.pop(0)  # Remove "fn"
                        n = 0
                        while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                            self.Vb()
                            n += 1
                        if self.tokens and self.tokens[0].value != ".":
                            print("Parse error at E : '.' Expected")
                        if self.tokens:
                            self.tokens.pop(0)  # Remove "."
                            self.E()
                            self.ast.append(Node(NodeType.lambda_expr, "lambda", n + 1))
                else:
                    # print('Entering else block...')
                    self.Ew()
            else:
                print("Invalid token format.")
        else:
            print("Tokens list is empty.")


    # Ew	->T 'where' Dr			=> 'where'
    # 		->T;

    def Ew(self):
        self.T()
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.ast.append(Node(NodeType.where, "where", 2))

    # Tuple Expressions

    # T 	-> Ta ( ',' Ta )+ => 'tau'
    # 		-> Ta ;
            
    def T(self):
        self.Ta()
        n = 1
        while self.tokens[0].value == ",":
            self.tokens.pop(0)  # Remove comma(,)
            self.Ta()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.tau, "tau", n))

    '''
    # Ta 	-> Ta 'aug' Tc => 'aug'
    # 		-> Tc ;
    Avoid left recursion by converting the grammar to right recursion
    Ta -> Tc ('aug' Tc)*
    '''
    def Ta(self):
        self.Tc()
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()
            self.ast.append(Node(NodeType.aug, "aug", 2))

    '''
    Tc 	-> B '->' Tc '|' Tc => '->'
     		-> B ;
    '''    
    def Tc(self):
        self.B()
        if self.tokens[0].value == "->":
            self.tokens.pop(0)  # Remove '->'
            self.Tc()
            if self.tokens[0].value != "|":
                print("Parse error at Tc: conditional '|' expected")
                # return
            self.tokens.pop(0)  # Remove '|'
            self.Tc()
            self.ast.append(Node(NodeType.conditional, "->", 3))
"""