from enum import Enum, auto
from "../Lexer/validToken" import validToken, validTokenTypes

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
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value  # Optional, for terminal values like identifier or integer

    def __repr__(self):
        if self.value is not None:
            return f"{self.node_type.name}({self.value})"
        elif self.children:
            return f"{self.node_type.name}({', '.join(map(str, self.children))})"
        else:
            return f"{self.node_type.name}"

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
            return ParseNode(NodeType.LAMBDA, vb_list + [e])
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
            return ParseNode(NodeType.conditional, [b, true_branch, false_branch])
        return b

    def parseB(self):
        bt = self.parseBt()
        while self.match(validTokenTypes.Keyword, 'or'):
            right = self.parseBt()
            bt = ParseNode(NodeType.op_or, [bt, right])
        return bt

    def parseBt(self):
        bs = self.parseBs()
        while self.match(validTokenTypes.Operator, '&'):
            right = self.parseBs()
            bs = ParseNode(NodeType.op_and, [bs, right])
        return bs

    def parseBs(self):
        if self.match(validTokenTypes.Keyword, 'not'):
            bp = self.parseBp()
            return ParseNode(NodeType.op_not, [bp])
        return self.parseBp()

    def parseBp(self):
        a1 = self.parseA()
        token = self.peek()
        if token and token.getType() == validTokenTypes.Keyword:
            if token.getContext() in ['gr', 'ge', 'ls', 'le', 'eq', 'ne']:
                self.advance()
                a2 = self.parseA()
                return ParseNode(NodeType.op_compare, [a1, a2])
        if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['>', '>=', '<', '<=']:
            self.advance()
            a2 = self.parseA()
            return ParseNode(NodeType.op_compare, [a1, a2])
        return a1

    def parseA(self):
        token = self.peek()
        if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['+', '-']:
            self.advance()
            at = self.parseAt()
            return ParseNode(NodeType.op_neg, [at])
        a = self.parseAt()
        while True:
            token = self.peek()
            if token and token.getType() == validTokenTypes.Operator and token.getContext() in ['+', '-']:
                op = token.getContext()
                self.advance()
                right = self.parseAt()
                node_type = NodeType.op_plus if op == '+' else NodeType.op_minus
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
                node_type = NodeType.op_mul if op == '*' else NodeType.op_div
                af = ParseNode(node_type, [af, right])
            else:
                break
        return af

    def parseAf(self):
        ap = self.parseAp()
        if self.match(validTokenTypes.Operator, '**'):
            right = self.parseAf()
            return ParseNode(NodeType.op_pow, [ap, right])
        return ap

    def parseAp(self):
        r = self.parseR()
        while self.match(validTokenTypes.Operator, '@'):
            id_token = self.expect(validTokenTypes.Identifier)
            rator = ParseNode(NodeType.identifier, [id_token])
            rand = self.parseR()
            r = ParseNode(NodeType.at, [r, rator, rand])
        return r
