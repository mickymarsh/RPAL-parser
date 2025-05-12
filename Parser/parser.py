from Parser.node import ParseNode, NodeType
from Lexer.validTokens import validToken, validTokenTypes

class ASTParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

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

    def expect(self, token_type, context=None):
        token = self.peek()
        if token and token.getType() == token_type and (context is None or token.getContext() == context):
            self.advance()
            return token
        raise SyntaxError(f"Expected token type {token_type} with context {context}, got {token}")
  
          

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
            return ParseNode(NodeType.gre, [b, true_branch, false_branch])
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
            # Fixed: Use the correct node type for unary operators
            node_type = NodeType.plus if token.getContext() == '+' else NodeType.neg
            return ParseNode(node_type, [at])
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
            # Fixed: Create identifier node with value, not with token as child
            rator = ParseNode(NodeType.identifier, value=id_token.getContext())
            rand = self.parseR()
            r = ParseNode(NodeType.at, [r, rator, rand])
        return r

    def parseR(self):
        rn = self.parseRn()
        token= self.peek()
        
        while token and self.could_start_rn(token):
            r = self.parseR()
            rn = ParseNode(NodeType.gamma, [rn, r])
            token = self.peek()  # Update token after parsing
        return rn
    
    def could_start_rn(self, token):
    
        if token.getType() == validTokenTypes.Keyword:
            return token.getContext() in ['true', 'false', 'nil', 'dummy']
        elif token.getType() in [validTokenTypes.Identifier, validTokenTypes.Integer, validTokenTypes.String]:
            return True
        elif token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            return True
        return False
    
    def parseRn(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            e = self.parseE()
            self.expect(validTokenTypes.Punction, ')')
            return e
        elif token and token.getType() == validTokenTypes.Keyword and token.getContext() == 'true':
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
        
        
        elif token:
            if token.getType() == validTokenTypes.Identifier:
                self.advance()
                return ParseNode(NodeType.identifier, value=token.getContext())
            elif token.getType() == validTokenTypes.Integer:
                self.advance()
                return ParseNode(NodeType.integer, value=token.getContext())
            elif token.getType() == validTokenTypes.String:
                self.advance()
                return ParseNode(NodeType.string, value=token.getContext())
        
        raise SyntaxError(f"Unexpected token: {token}")

    def parseD(self):
        da = self.parseDa()
        while self.match(validTokenTypes.Keyword, 'within'):
            # Fixed: Removed extra advance() call
            d = self.parseD()
            da = ParseNode(NodeType.within, [da, d])
        return da
    
    def parseDa(self):
        dr = self.parseDr()
        nodes = [dr]
        while self.match(validTokenTypes.Keyword, 'and'):
            nodes.append(self.parseDr())
        if len(nodes) > 1:
            return ParseNode(NodeType.andop, nodes)
        return dr
    
    def parseDr(self):
        if self.match(validTokenTypes.Keyword, 'rec'):
            db = self.parseDb()
            return ParseNode(NodeType.rec, [db])
        return self.parseDb()
    
    def parseDb(self):
        token = self.peek()
        # Fixed: Check for "Vl" operator
        if token and token.getType() == validTokenTypes.Operator and token.getContext() == "Vl":
            self.advance()
            vl = self.parseVl()
            self.expect(validTokenTypes.Operator, '=')
            e = self.parseE()
            return ParseNode(NodeType.equal, [vl, e])
        elif token and token.getType() == validTokenTypes.Identifier:
            id_token = self.expect(validTokenTypes.Identifier)
            # Fixed: Create identifier node with value, not with token as child
            rator = ParseNode(NodeType.identifier, value=id_token.getContext())
            # Fixed: Removed extra advance() call
            vb_list = []
            while True:
                if self.peek() and self.peek().getType() == validTokenTypes.Operator and self.peek().getContext() == '=':
                    self.advance()
                    break
                vb = self.parseVb()
                vb_list.append(vb)
            
            e = self.parseE()
            # Fixed: Corrected parameter order for fcn_form
            return ParseNode(NodeType.fcn_form, [rator] + vb_list + [e])
        
        elif token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            d = self.parseD()
            self.expect(validTokenTypes.Punction, ')')
            return d
        
        raise SyntaxError(f"Unexpected token in parseDb: {token}")
    
    def parseVb(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Punction and token.getContext() == '(':
            self.advance()
            if self.match(validTokenTypes.Punction, ')'):
                return ParseNode(NodeType.empty_params)
            else:
                vl = self.parseVl()
                self.expect(validTokenTypes.Punction, ')')
                return vl
        elif token and token.getType() == validTokenTypes.Identifier:
            self.advance()
            return ParseNode(NodeType.identifier, value=token.getContext())
        
        raise SyntaxError(f"Unexpected token in parseVb: {token}")
    
    def parseVl(self):
        nodes = []
        while True:
            token = self.peek()
            if token and token.getType() == validTokenTypes.Identifier:
                self.advance()
                nodes.append(ParseNode(NodeType.identifier, value=token.getContext()))
                if not self.match(validTokenTypes.Punction, ','):
                    break
            else:
                break
        if len(nodes) == 1:
            return nodes[0]
        return ParseNode(NodeType.comma, nodes)

    def parse(self):
        return self.parseE()