from enum import Enum, auto
from Lexer.validTokens import validToken, validTokenTypes

class NodeType(Enum):
    let = auto()
    lambda_ = auto()     # 'lambda' is a Python keyword, so we use lambda_
    where = auto()
    tau = auto()
    aug = auto()
    arrow = auto()       # for '->' expression
    or_ = auto()         # 'or' is also a Python keyword
    and_ = auto()
    not_ = auto()
    gr = auto()
    ge = auto()
    ls = auto()
    le = auto()
    eq = auto()
    ne = auto()
    plus = auto()
    minus = auto()
    neg = auto()
    mul = auto()
    div = auto()
    pow = auto()         # for '**'
    at = auto()
    gamma = auto()
    true = auto()
    false = auto()
    nil = auto()
    dummy = auto()
    within = auto()
    andop = auto()       # distinguish definition-level 'and'
    rec = auto()
    equal = auto()
    fcn_form = auto()
    identifier = auto()
    integer = auto()
    string = auto()
    comma = auto()
    empty_params = auto()

class ParseNode:
    def __init__(self, node_type, children=None, value=None,tokens=None):
        self.tokens = tokens
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value  # Optional, for terminal values like identifier or integer
        self.pos = 0  # Initialize position for token tracking

    def __repr__(self):
        if self.value is not None:
            return f"{self.node_type.name}({self.value})"
        elif self.children:
            return f"{self.node_type.name}({', '.join(map(str, self.children))})"
        else:
            return f"{self.node_type.name}"
        
    # def print_tree(self, indent=0):
    #     """Recursively print the parse tree with proper indentation."""
    #     # Print the current node with indentation
    #     print('  ' * indent + str(self))
        
    #     # Check if children is a list or iterable
    #     if self.children:
    #         # If children is a list, iterate through it
    #         if isinstance(self.children, list):
    #             for child in self.children:
    #                 child.print_tree(indent + 1)
    #         # If children is a single node, print it
    #         else:
    #             self.children.print_tree(indent + 1)

    def print_tree(self, indent=0):
        """Recursively print the parse tree with proper indentation."""
        # Print the current node with indentation
        print('  ' * indent + str(self))
        
        # Check if children is a list or iterable
        if self.children:
            # If children is a list, iterate through it
            if isinstance(self.children, list):
                for child in self.children:
                    # Check if child is None before calling print_tree
                    if child is not None:
                        child.print_tree(indent + 1)
                    else:
                        print('  ' * (indent + 1) + "None")
            # If children is a single node, print it if not None
            elif self.children is not None:
                self.children.print_tree(indent + 1)
            else:
                print('  ' * (indent + 1) + "None")
        
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def match(self, token_type, context=None):
        token = self.peek()
        if token and token.getType() == token_type and (context is None or token.getContext() == context):
            self.advance()
            return True
        return False

    def parseE(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'let':
            self.advance()
            d = self.parseD()
            self.expect(validTokenTypes.Keyword, 'in')
            e = self.parseE()
            return ParseNode(NodeType.let, [d, e])
        elif token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'fn':
            self.advance()
            vb_list = []
            while True:
                vb = self.parseVb()
                vb_list.append(vb)
                if self.match(validTokenTypes.Operator, '.'):
                    break
            e = self.parseE()
            return ParseNode(NodeType.lambda_, vb_list + [e])
        else:
            return self.parseEw()

    def parseEw(self):
        t = self.parseT()
        if self.match(validTokenTypes.Keyword, 'where'):
            dr = self.parseDr()
            return ParseNode(NodeType.where, [t, dr])
        return t

    def parseT(self):
        ta = self.parseTa()
        nodes = [ta]
        while self.match(validTokenTypes.Punction, ','):
            nodes.append(self.parseTa())
        if len(nodes) > 1:
            return ParseNode(NodeType.tau, nodes)
        return ta

    def parseTa(self):
        tc = self.parseTc()
        nodes = [tc]
        while self.match(validTokenTypes.Keyword, 'aug'):
            nodes.append(self.parseTc())
        if len(nodes) > 1:
            return ParseNode(NodeType.aug, nodes)
        return tc

    def parseTc(self):
        b = self.parseB()
        if self.match(validTokenTypes.Operator, '->'):
            true_branch = self.parseTc()
            self.expect(validTokenTypes.Operator, '|')
            false_branch = self.parseTc()
            return ParseNode(NodeType.arrow, [b, true_branch, false_branch])
        return b

    def parseB(self):
        bt = self.parseBt()
        while self.match(validTokenTypes.Keyword, 'or'):
            right = self.parseBt()
            bt = ParseNode(NodeType.or_, [bt, right])
        return bt

    def parseBt(self):
        bs = self.parseBs()
        while self.match(validTokenTypes.Operator, '&'):
            right = self.parseBs()
            bs = ParseNode(NodeType.and_, [bs, right])
        return bs

    def parseBs(self):
        if self.match(validTokenTypes.Keyword, 'not'):
            bp = self.parseBp()
            return ParseNode(NodeType.not_, [bp])
        return self.parseBp()

    def parseBp(self):
        a1 = self.parseA()
        token = self.peek()
        if token and token.getType() == validTokenTypes.Keyword:
            if token.getContext() in ['gr', 'ge', 'ls', 'le', 'eq', 'ne']:
                self.advance()
                a2 = self.parseA()
                if token.getContext() == 'gr':
                    return ParseNode(NodeType.gr, [a1, a2])
                elif token.getContext() == 'ge':
                    return ParseNode(NodeType.ge, [a1, a2])
                elif token.getContext() == 'ls':
                    return ParseNode(NodeType.ls, [a1, a2])
                elif token.getContext() == 'le':
                    return ParseNode(NodeType.le, [a1, a2])
                elif token.getContext() == 'eq':
                    return ParseNode(NodeType.eq, [a1, a2])
                elif token.getContext() == 'ne':
                    return ParseNode(NodeType.ne, [a1, a2])
        if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['>', '>=', '<', '<=']:
            self.advance()
            a2 = self.parseA()
            if token.getContext() == '>':
                return ParseNode(NodeType.gr, [a1, a2])
            elif token.getContext() == '>=':
                return ParseNode(NodeType.ge, [a1, a2])
            elif token.getContext() == '<':
                return ParseNode(NodeType.ls, [a1, a2])
            elif token.getContext() == '<=':
                return ParseNode(NodeType.le, [a1, a2])
            
        return a1

    def parseA(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['+', '-']:
            self.advance()
            at = self.parseAt()
            return ParseNode(NodeType.neg, [at])
        a = self.parseAt()
        while True:
            token = self.peek()
            if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['+', '-']:
                op = token.getContext()
                self.advance()
                right = self.parseAt()
                node_type = NodeType.plus if op == '+' else NodeType.minus
                a = ParseNode(node_type, [a, right])
            else:
                break
        return a

    def parseAt(self):
        af = self.parseAf()
        while True:
            token = self.peek()
            if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['*', '/']:
                op = token.getContext()
                self.advance()
                right = self.parseAf()
                node_type = NodeType.mul if op == '*' else NodeType.div
                af = ParseNode(node_type, [af, right])
            else:
                break
        return af

    def parseAf(self):
        ap = self.parseAp()
        if self.match(validTokenTypes.Operator, '**'):
            right = self.parseAf()
            return ParseNode(NodeType.pow, [ap, right])
        return ap

    def parseAp(self):
        r = self.parseR()
        while self.match(validTokenTypes.Operator, '@'):
            id_token = self.expect(validTokenTypes.Identifier)
            rator = ParseNode(NodeType.identifier, [id_token])
            rand = self.parseR()
            r = ParseNode(NodeType.at, [r, rator, rand])
        return r

    def parseR(self):
        rn=self.parseRn()
        while self.match(validTokenTypes.Keyword, 'gamma'):
            self.advance()
            r=self.parseR()
            rn=ParseNode(NodeType.gamma,[rn,r])
        return rn
    
    def parseRn(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'true':
            self.advance()
            return ParseNode(NodeType.true)
        elif token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'false':
            self.advance()
            return ParseNode(NodeType.false)
        elif token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'nil':
            self.advance()
            return ParseNode(NodeType.nil)
        elif token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'dummy':
            self.advance()
            return ParseNode(NodeType.dummy)
        
        elif token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            e = self.parseE()  # Parse the expression inside parentheses
            self.expect(validTokenTypes.Punction, ')')  # Ensure closing parenthesis
            return e
        
        elif (token := self.peek()) is not None:
            if (token_type := token.getType()) in {validTokenTypes.Identifier, validTokenTypes.Integer, validTokenTypes.String}:
                self.advance()
                return ParseNode(
                    NodeType.identifier if token_type == validTokenTypes.Identifier else
                    NodeType.integer if token_type == validTokenTypes.Integer else
                    NodeType.string,
                    value=token.getContext())
    

    def parseD(self):
        da=self.parseDa()
        while self.match(validTokenTypes.Keyword,'within'):
            self.advance()
            d=self.parseD()
            da=ParseNode(NodeType.within,[da,d])
        return da
    
    def parseDa(self):
        dr=self.parseDr()
        nodes=[dr]
        while self.match(validTokenTypes.Keyword,'and'):
            nodes.append(self.parseDr())
        if len(nodes)>1:
            return ParseNode(NodeType.andop,nodes)
        return dr
    
    def parseDr(self):
        
        if self.match(validTokenTypes.Keyword,'rec'):
            db=self.parseDb()
            
            return ParseNode(NodeType.rec,[db])
        return self.parseDb()
    
    def parseDb(self):
        token=self.peek()
        if token and token.getType() == validTokenTypes.Operator and token.getContext() == "Vl":
            self.advance()
            vl=self.parseVl()
            self.expect(validTokenTypes.Operator,'=')
            e=self.parseE()
            return ParseNode(NodeType.equal,[vl,e])
        elif token and token.getType() == validTokenTypes.Identifier:
            id_token = self.expect(validTokenTypes.Identifier)
            rator = ParseNode(NodeType.identifier, [id_token])
            self.advance()
            vb_list = []
            while True:
                
                if self.peek().getType() == validTokenTypes.Operator and self.peek().getContext() == '=':
                    self.advance()
                    break
                vb = self.parseVb()
                vb_list.append(vb)
            
            e = self.parseE()
            return ParseNode(NodeType.fcn_form,rator, vb_list + [e])
        
        elif token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            d = self.parseD()  # Parse the expression inside parentheses
            self.expect(validTokenTypes.Punction, ')')  # Ensure closing parenthesis
            return d

        
    def parseVb(self):
        token=self.peek()
        if token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            if self.match(validTokenTypes.Punction, ')'):
                return ParseNode(NodeType.empty_params)
            else:
                vl = self.parseVl()
                self.expect(validTokenTypes.Punction, ')')  # Ensure closing parenthesis
                return vl
        elif token and token.getType() == validTokenTypes.Identifier:
        
            self.advance()
            return ParseNode(NodeType.identifier, value=token.getContext())
        
    
    def parseVl(self):
        nodes = []
        while True:
            token = self.peek()
            if token and token.getType() == validTokenTypes.Identifier:
                self.advance()
                nodes.append(ParseNode(NodeType.identifier, value=token.getContext()))
                if not self.match(validTokenTypes.Punction, ','):  # Check for a comma
                    break
            else:
                break
        if len(nodes) == 1:
            return nodes[0]  # Return a single identifier if there's no list
        return ParseNode(NodeType.comma, nodes)  # Return a node representing the list

        
        
    def expect(self, token_type, context=None):
        token = self.peek()
        if not token or token.getType() != token_type or (context and token.getContext() != context):
            raise SyntaxError(f"Expected {token_type} {context}, but got {token}")
        self.advance()

    def parse(self):
        return self.parseE()   
    


    
    
        


            
    

        
        
