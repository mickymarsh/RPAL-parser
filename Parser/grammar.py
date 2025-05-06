from Parser.build_ast import TreeBuilder
from Parser.node import Node  
from Lexer.validTokens import validTokenTypes, validToken

class Parser:
    def __init__(self, tokens: list[validToken]):
        self.tokens = tokens
        self.builder = TreeBuilder()

    def parse(self):
        print("parsing started")
        self.tokens.append(validToken(validTokenTypes.End_of_tokens, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        if self.tokens[0].type == validTokenTypes.End_of_tokens:
            return self.builder.stack
        else:
            print("Parsing Unsuccessful!...........")
            

    # Expressions 
                
    # E	->'let' D 'in' E		=> 'let'
    # 	->'fn' Vb+ '.' E		=> 'lambda'
    # 	->Ew;

    def E(self):
        print("welcome to section E")
        if self.tokens:  # Ensure tokens list is not empty
            token = self.tokens[0]
            if hasattr(token, 'tokenType') and hasattr(token, 'context'):  # Check if token has type and value attributes
                if token.tokenType == validTokenTypes.Keyword and token.context in ["let", "fn"]:
                    if token.context == "let":
                        self.tokens.pop(0)  # Remove "let"
                        self.D()
                        if self.tokens[0].context != "in":
                            print("Parse error at E : 'in' Expected")
                        self.tokens.pop(0)  # Remove "in"
                        self.E()
                        self.builder.build_tree('let',2)
                    else:
                        self.tokens.pop(0)  # Remove "fn"
                        n = 0
                        while self.tokens and (self.tokens[0].tokenType == validTokenTypes.Identifier or self.tokens[0].context == "("):
                            self.Vb()
                            n += 1
                        if self.tokens and self.tokens[0].context != ".":
                            print("Parse error at E : '.' Expected")
                        if self.tokens:
                            self.tokens.pop(0)  # Remove "."
                            self.E()
                            self.builder.build_tree('lambda', n+1)
                else:
                    self.Ew()
            else:
                print("Invalid token format.")
        else:
            print("Tokens list is empty.")


    
    # Ew	->T 'where' Dr			=> 'where'
    # 		->T;

    def Ew(self):
        self.T()
        if self.tokens[0].context == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.builder.build_tree('where', 2)

    # Tuple Expressions

    # T 	-> Ta ( ',' Ta )+ => 'tau'
    # 		-> Ta ;
            
    def T(self):
        self.Ta()
        n = 1
        while self.tokens[0].context == ",":
            self.tokens.pop(0)  # Remove comma(,)
            self.Ta()
            n += 1
        if n > 1:
            self.builder.build_tree('tau',n)

    '''
    # Ta 	-> Ta 'aug' Tc => 'aug'
    # 		-> Tc ;
    Avoid left recursion by converting the grammar to right recursion
    Ta -> Tc ('aug' Tc)*
    '''
    def Ta(self):
        self.Tc()
        while self.tokens[0].context == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()
            self.builder.build_tree('aug',2)

    '''
    Tc 	-> B '->' Tc '|' Tc => '->'
     		-> B ;
    '''    
    def Tc(self):
        self.B()
        if self.tokens[0].context == "->":
            self.tokens.pop(0)  # Remove '->'
            self.Tc()
            if self.tokens[0].context != "|":
                print("Parse error at Tc: conditional '|' expected")
                # return
            self.tokens.pop(0)  # Remove '|'
            self.Tc()
            self.builder.build_tree('->', 3)
