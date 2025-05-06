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
        if self.tokens[0].tokenType == validTokenTypes.End_of_tokens:
            print("Parsing successful")
            return self.builder.stack
        else:
            print("Parsing Unsuccessful!...........")
            

    # Expressions 
                
    # E	->'let' D 'in' E		=> 'let'
    # 	->'fn' Vb+ '.' E		=> 'lambda'
    # 	->Ew;

    def E(self):
        print("welcome to section E")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        if self.tokens:  # Ensure tokens list is not empty
            token = self.tokens[0]
            if hasattr(token, 'tokenType') and hasattr(token, 'context'):  # Check if token has type and value attributes
                if token.tokenType == validTokenTypes.Keyword and token.context in ["let", "fn"]:
                    if token.context == "let":
                        self.tokens.pop(0)  # Remove "let"
                        self.D()
                        print("finally come back to E after let \n")
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
                    print("come back to E after Ew \n")
            else:
                print("Invalid token format.")
        else:
            print("Tokens list is empty.")


    
    # Ew	->T 'where' Dr			=> 'where'
    # 		->T;

    def Ew(self):
        print("welcome to section Ew")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.T()
        print("Back in Ew after T ")
        print("Now in Ew the top token is : ", self.tokens[0].context, "\n")
        if self.tokens[0].context == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.builder.build_tree('where', 2)

    # Tuple Expressions

    # T 	-> Ta ( ',' Ta )+ => 'tau'
    # 		-> Ta ;
            
    def T(self):
        print("welcome to section T")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Ta()
        print("Back in T after Ta \n")
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
        print("welcome to section Ta")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Tc()
        print("Back in Ta after Tc \n")
        while self.tokens[0].context == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()
            self.builder.build_tree('aug',2)

    '''
    Tc 	-> B '->' Tc '|' Tc => '->'
     		-> B ;
    '''    
    def Tc(self):
        print("welcome to section Tc")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.B()
        print("Back in Tc after B \n")
        if self.tokens[0].context == "->":
            self.tokens.pop(0)  # Remove '->'
            self.Tc()
            if self.tokens[0].context != "|":
                print("Parse error at Tc: conditional '|' expected")
                # return
            self.tokens.pop(0)  # Remove '|'
            self.Tc()
            self.builder.build_tree('->', 3)

    # Boolean Expressions
    '''
    # B 	-> B 'or' Bt 	=> 'or'
    #     -> Bt ;	
    
    B -> Bt ('or' Bt)*
    '''
    def B(self):
        print("welcome to section B")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Bt()
        print("Back in B after Bt \n")
        while self.tokens[0].context == "or":
            self.tokens.pop(0)  # Remove 'or'
            self.Bt()
            self.builder.build_tree('or', 2)

    '''
    # Bt	-> Bt '&' Bs => '&'
    # 			-> Bs ;
    
    Bt -> Bs ('&' Bs)*
    '''
    def Bt(self):
        print("welcome to section Bt")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Bs()
        print("Back in Bt after Bs \n")
        while self.tokens[0].context == "&":
            self.tokens.pop(0)  # Remove '&'
            self.Bs()
            self.builder.build_tree('&', 2)

    # Bs	-> 'not' Bp => 'not'
    # 		-> Bp ;

    def Bs(self):
        print("welcome to section Bs")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        if self.tokens[0].context == "not":
            self.tokens.pop(0)  # Remove 'not'
            self.Bp()
            print("Back in Bs after Bp \n")
            self.builder.build_tree('not', 1)
            print("Build a tree in Bs \n")
        else:
            self.Bp()
            print("Back in Bs after Bp \n")

    #  Bp 	-> A ('gr' | '>' ) A => 'gr'
    # 			-> A ('ge' | '>=') A => 'ge'
    # 			-> A ('ls' | '<' ) A => 'ls'
    # 			-> A ('le' | '<=') A => 'le'
    # 			-> A 'eq' A => 'eq'
    # 			-> A 'ne' A => 'ne'
    # 			-> A ;
            

    def Bp(self):
        print("welcome to section Bp")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.A()
        print("Back in Bp after A \n")
        print("Now the top token is : ", self.tokens[0].context, "\n")

        token = self.tokens[0]
        if token.context in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            self.tokens.pop(0)
            self.A()
            print("Now the top token is : ", self.tokens[0].context, "\n")

            if token.context == ">":
                self.builder.build_tree('gr', 3)
            elif token.context == ">=":
                self.builder.build_tree('ge', 3)
            elif token.context == "<":
                self.builder.build_tree('ls', 3)
            elif token.context == "<=":
                self.builder.build_tree('le', 3)
            else:
                self.builder.build_tree(token.context, 3)

    # Arithmetic Expressions

    # A 	-> A '+' At => '+'
    # 		-> A '-' At => '-'
    # 		-> '+' At
    # 		-> '-'At =>'neg'
    # 		-> At ;

    def A(self):
        print("welcome to section A")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        if self.tokens[0].context == "+":
            self.tokens.pop(0)  # Remove unary plus
            self.At()
            print("Back in A after At \n")
        elif self.tokens[0].context == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            print("Back in A after At \n")
            self.builder.build_tree('neg', 1)
        else:
            self.At()
            print("Back in A after At \n")

        while self.tokens[0].context in {"+", "-"}:
            current_token = self.tokens[0]  # Save present token
            self.tokens.pop(0)  # Remove plus or minus operators
            self.At()
            if current_token.value == "+":
                self.builder.build_tree('+', 2)
            else:
                self.builder.build_tree('-', 2)

    '''
    At 	-> At '*' Af => '*'
    				-> At '/' Af => '/'
    				-> Af ;

    At -> Af ('*' Af | '/' Af)*
    '''           
    def At(self):
        print("welcome to section At")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Af()
        print("Back in At after Af \n")
        while self.tokens[0].context in {"*", "/"}:
            current_token = self.tokens[0]  # Save present token
            self.tokens.pop(0)  # Remove multiply or divide operators
            self.Af()
            if current_token.context == "*":
                self.builder.build_tree('*', 2)
            else:
                self.builder.build_tree('/', 2)

    '''
    Af 	-> Ap '**' Af => '**'
    				-> Ap ;
        
    Af -> Ap ('**' Af)*
    '''

    def Af(self):
        print("welcome to section Af")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Ap()

        print("Back in Af after Ap \n")

        if self.tokens[0].context == "**":
            self.tokens.pop(0)  # Remove power operator
            self.Af()
            self.builder.build_tree('**', 2)

    '''
    Ap 	-> Ap '@' '<IDENTIFIER>' R => '@'
    				-> R ;
    
    Ap -> R ('@' '<IDENTIFIER>' R)*
    '''   
    def Ap(self):
        print("welcome to section Ap")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.R()
        print("Back in Ap after R \n")
        while self.tokens[0].context == "@":
            self.tokens.pop(0)  # Remove @ operator
            
            if self.tokens[0].tokenType != validTokenTypes.Identifier:
                print("Parsing error at Ap: IDENTIFIER EXPECTED")
                # Handle parsing error here
                return
            
            self.builder.build_tree(self.tokens[0].context, 0)
            self.tokens.pop(0)  # Remove IDENTIFIER
            
            self.R()
            self.builder.build_tree('@', 3)

    # Rators And Rands
    '''
    R 	-> R Rn => 'gamma'
    		-> Rn ;
    
    R -> Rn ('gamma' Rn)*
    '''
            
    def R(self):
        print("welcome to section R")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Rn()
        print("Back in R after Rn \n")
        while (self.tokens[0].tokenType in [validTokenTypes.Identifier, validTokenTypes.Integer, validTokenTypes.String] or
            self.tokens[0].context in ["true", "false", "nil", "dummy"] or
            self.tokens[0].context == "("):
            
            self.Rn()
            self.builder.build_tree('gamma', 2)

    #        Rn 	-> '<IDENTIFIER>'
    # 				-> '<INTEGER>'
    # 				-> '<STRING>'
    # 				-> 'true' => 'true'
    # 				-> 'false' => 'false'
    # 				-> 'nil' => 'nil'
    # 				-> '(' E ')'
    # 				-> 'dummy' => 'dummy' ;
            
    def Rn(self):
        print("welcome to section Rn")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        token_type = self.tokens[0].tokenType
        token_value = self.tokens[0].context

        # print(f"Processing token: {token_type}, {token_value}")
        
        if token_type == validTokenTypes.Identifier:
            self.builder.build_tree(token_value, 0)
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == validTokenTypes.Integer:
            self.builder.build_tree(token_value, 0)
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == validTokenTypes.String:
            self.builder.build_tree(token_value, 0)
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == validTokenTypes.Keyword:
            if token_value == "true":
                self.builder.build_tree(token_value, 0)
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "false":
                self.builder.build_tree(token_value, 0)
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "nil":
                self.builder.build_tree(token_value, 0)
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "dummy":
                self.builder.build_tree(token_value, 0)
                # print(token_value)
                self.tokens.pop(0)
            else:
                print("Parse Error at Rn: Unexpected KEYWORD")
        elif token_type == validTokenTypes.Punction:
            if token_value == "(":
                # # print(token_value)
                self.tokens.pop(0)  # Remove '('
                
                self.E()
                
                if self.tokens[0].context != ")":
                    print("Parsing error at Rn: Expected a matching ')'")
                    # return
                # # print(tokens[0].value)
                self.tokens.pop(0)  # Remove ')'
            else:
                print("Parsing error at Rn: Unexpected PUNCTUATION")
        else:
            print(token_type, token_value)
            print("Parsing error at Rn: Expected a Rn, but got different")

    # Definitions

    # D 	-> Da 'within' D => 'within'
    # 				-> Da ;
            
    def D(self):
        
        print("welcome to section D")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Da()
        if self.tokens[0].context == "within":
            # # print(tokens[0].value)
            self.tokens.pop(0)  # Remove 'within'
            self.D()
            self.builder.build_tree('within', 2)

    # Da  -> Dr ( 'and' Dr )+ => 'and'
    # 					-> Dr ;
            
    def Da(self): 
        print("welcome to section Da")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        self.Dr()
        n = 1
        while self.tokens[0].context == "and":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            self.Dr()
            n += 1
        if n > 1:
            self.builder.build_tree('and', n)

    # Dr  -> 'rec' Db => 'rec'
    # 	-> Db ;
            
    def Dr(self):
        print("welcome to section Dr")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        is_rec = False
        if self.tokens[0].context == "rec":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            is_rec = True
        self.Db()
        if is_rec:
            self.builder.build_tree('rec', 1)

    # Db  -> Vl '=' E => '='
    # 				-> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
    # 				-> '(' D ')' ; 
            
    def Db(self): 
        print("welcome to section Db")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        if self.tokens[0].tokenType == validTokenTypes.Punction and self.tokens[0].context == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].context != ")":
                print("Parsing error at Db #1")
                # return
            # print(tokens[0].value)
            self.tokens.pop(0)
        elif self.tokens[0].tokenType == validTokenTypes.Identifier:
            # print(self.tokens[0].value)
            if self.tokens[1].context == "(" or self.tokens[1].tokenType == validTokenTypes.Identifier:
                # Expect a fcn_form
                self.builder.build_tree(self.tokens[0].context, 0)
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove ID

                n = 1  # Identifier child
                while self.tokens[0].tokenType == validTokenTypes.Identifier or self.tokens[0].context == "(":
                    self.Vb()
                    n += 1
                if self.tokens[0].context != "=":
                    print("Parsing error at Db #2")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.E()
                print("come back to Db after E")

                self.builder.build_tree('fcn_form', n)

            elif self.tokens[1].context == "=":
                self.builder.build_tree(self.tokens[0].context, 0)
                # print(tokens[0].value)
                self.tokens.pop(0)  # Remove identifier
                # print(tokens[0].value)
                self.tokens.pop(0)  # Remove equal
                self.E()
                self.builder.build_tree('=', 2)
            elif self.tokens[1].context == ",":
                self.Vl()
                if self.tokens[0].context != "=":
                    print("Parsing error at Db")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.E()

                self.builder.build_tree('=', 2)

    # Variables
                
    # Vb  -> '<IDENTIFIER>'
    # 	  -> '(' Vl ')'
    # 	  -> '(' ')' => '()';

    def Vb(self):
        print("welcome to section Vb")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        if self.tokens[0].tokenType == validTokenTypes.Punction and self.tokens[0].context == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            isVl = False

            if self.tokens[0].tokenType == validTokenTypes.Identifier:
                # print(self.tokens[0].value)
                self.Vl()
                isVl = True
            
            if self.tokens[0].context != ")":
                print("Parse error unmatch )")
                # return
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            if not isVl:
                self.builder.build_tree('()', 0)

        elif self.tokens[0].tokenType == validTokenTypes.Identifier:
            print("in Vb i identify x as an identifier")
            
            self.builder.build_tree(self.tokens[0].context, 0)
            self.tokens.pop(0)

            print(self.tokens[0].context, "this is the new top after build the tree \n")

            

    # Vl -> '<IDENTIFIER>' list ',' => ','?;
            
    def Vl(self):
        print("welcome to section Vl")
        print("Now the top token is : ", self.tokens[0].context, "\n")
        n = 0
        while True:
            # print(self.tokens[0].value)
            if n > 0:
                self.tokens.pop(0)
            if not self.tokens[0].tokenType == validTokenTypes.Identifier:
                print("Parse error: an identifier was expected")
            # print(self.tokens[0].value)
            self.builder.build_tree(self.tokens[0].context, 0)
            
            self.tokens.pop(0)
            n += 1
            if not self.tokens[0].context == ",":
                break
        
        if n > 1:
            self.builder.build_tree(',', n)