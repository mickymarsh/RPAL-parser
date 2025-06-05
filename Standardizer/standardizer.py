from Parser.node import ParseNode, NodeType
from Standardizer.st_node import STNode, STNodeType

class Standardizer:
    def standardize(self, node: ParseNode) -> STNode:

        # First, recursively standardize all children (bottom-up approach)
        standardized_children = []
        for child in node.children:
            standardized_children.append(self.standardize(child))
        
        # Create a temporary node with standardized children for transformation
        temp_node = ParseNode(node.node_type, standardized_children, node.value)

        if node.node_type == NodeType.let:
            return self._standardize_let(temp_node)
        elif node.node_type == NodeType.where:
            return self._standardize_where(temp_node)
        elif node.node_type == NodeType.fcn_form:
            return self._standardize_function_form(temp_node)
        elif node.node_type == NodeType.lambda_:
            return self._standardize_lambda(temp_node)
        elif node.node_type == NodeType.tau:
            return self._standardize_tuple(temp_node)
        elif node.node_type == NodeType.within:
            return self._standardize_within(temp_node)
        elif node.node_type == NodeType.rec:
            return self._standardize_rec(temp_node)
        elif node.node_type == NodeType.at:
            return self._standardize_at(temp_node)
        elif node.node_type == NodeType.andop:
            return self._standardize_and(temp_node)
        elif node.node_type == NodeType.gre:
            return self._standardize_cond(temp_node)
        elif node.node_type == NodeType.comma:
            return self._standardize_comma(temp_node)
        elif node.node_type in [
            NodeType.aug, NodeType.or_, NodeType.and_, NodeType.not_,
            NodeType.plus, NodeType.minus, NodeType.neg, NodeType.mul,
            NodeType.div, NodeType.pow, NodeType.gr, NodeType.ge,
            NodeType.ls, NodeType.le, NodeType.eq, NodeType.ne
        ]:
            return self._standardize_operator(temp_node)
        elif node.node_type == NodeType.equal:
            return self._standardize_equal(temp_node)
        elif node.node_type in [NodeType.identifier, NodeType.integer, NodeType.string]:
            return self._standardize_terminal(temp_node)
        elif node.node_type == NodeType.nil:
            return STNode(STNodeType.NIL)
        elif node.node_type == NodeType.true:
            return STNode(STNodeType.TRUE)
        elif node.node_type == NodeType.false:
            return STNode(STNodeType.FALSE)
        
        else:
            # default: gamma chain
            if len(node.children) == 2:
                gamma_node = STNode(STNodeType.GAMMA)
                gamma_node.add_child(self.standardize(node.children[0]))
                gamma_node.add_child(self.standardize(node.children[1]))
                return gamma_node
            else:
                raise Exception(f"Unhandled node type: {node.node_type}")

    

    def _standardize_where(self, node):
        gamma= STNode(STNodeType.GAMMA)
        lam = STNode(STNodeType.LAMBDA)
        lam.add_child(node.children[1].children[0])
        lam.add_child(node.children[0])
        gamma.add_child(lam)
        gamma.add_child(node.children[1].children[1])
        return gamma

    def _standardize_function_form(self, node):
        ident = (node.children[0])
        body = (node.children[-1])
        for param in reversed(node.children[1:-1]):
            lam = STNode(STNodeType.LAMBDA)
            lam.add_child(param)
            lam.add_child(body)
            body = lam
        eq = STNode(STNodeType.EQ)
        eq.add_child(ident)
        eq.add_child(body)
        return eq


    def _standardize_tuple(self, node):
        # Case for single-element tuple: just return the single element
        # if len(node.children) == 1:
        #     return (node.children[0])

        # Start with innermost: gamma(aug, nil)
        # inner_gamma = STNode(STNodeType.GAMMA)
        # inner_gamma.add_child(STNode(STNodeType.AUG))
        # inner_gamma.add_child(STNode(STNodeType.NIL))

        # Build nested gamma chain with each child expression
        # for child in node.children[:-1]:
        #     gamma = STNode(STNodeType.GAMMA)
        #     gamma.add_child(inner_gamma)
        #     gamma.add_child(child)
        #     inner_gamma = gamma

        # Finally wrap the last expression (e.g., E2)
        # outer_gamma = STNode(STNodeType.GAMMA)
        # outer_gamma.add_child(inner_gamma)
        # outer_gamma.add_child(node.children[-1])

        # return outer_gamma

        tau=STNode(STNodeType.TAU)
        for child in node.children:
            if child.node_type == NodeType.nil:
                tau.add_child(STNode(STNodeType.NIL))
            else:
                tau.add_child(child)

        return tau

    def _standardize_within(self, node):
        x1 = (node.children[0].children[0])
        e1 = (node.children[0].children[1])
        x2 = (node.children[1].children[0])
        e2 = (node.children[1].children[1])
        lam = STNode(STNodeType.LAMBDA)
        lam.add_child(x1)
        lam.add_child(e2)
        gamma = STNode(STNodeType.GAMMA)
        gamma.add_child(lam)
        gamma.add_child(e1)
        eq = STNode(STNodeType.EQ)
        eq.add_child(x2)
        eq.add_child(gamma)
        return eq

    def _standardize_rec(self, node):
        x = (node.children[0].children[0])
        e = (node.children[0].children[1])
        lam = STNode(STNodeType.LAMBDA)
        lam.add_child(x)
        lam.add_child(e)
        ystar = STNode(STNodeType.YSTAR)
        gamma = STNode(STNodeType.GAMMA)
        gamma.add_child(ystar)
        gamma.add_child(lam)
        eq = STNode(STNodeType.EQ)
        eq.add_child(x)
        eq.add_child(gamma)
        return eq

    def _standardize_at(self, node):
        gamma2 = STNode(STNodeType.GAMMA)
        gamma1 = STNode(STNodeType.GAMMA)
        gamma2.add_child(gamma1)
        gamma2.add_child(node.children[2])
        gamma1.add_child(node.children[1])
        gamma1.add_child(node.children[0])
        return gamma2

    def _standardize_and(self, node):
        comma = STNode(STNodeType.COMMA)
        tau = STNode(STNodeType.TAU)
        for child in node.children:
            for ele in child.children[0].children[0:]:
                comma.add_child(ele)
            for ele in child.children[1].children[0:]:
                tau.add_child(ele)
        eq = STNode(STNodeType.EQ)
        eq.add_child(comma)
        eq.add_child(tau)
        return eq

    def _standardize_comma(self, node):
        comma = STNode(STNodeType.COMMA)
        for child in node.children:
            if child.node_type == NodeType.nil:
                comma.add_child(STNode(STNodeType.NIL))
            else:
                comma.add_child(child)
        return comma
    
    def _standardize_cond(self, node):
        b = (node.children[0])
        t = (node.children[1])
        e = (node.children[2])

        cond = STNode(STNodeType.COND)
        cond.add_child(b)
        cond.add_child(t)
        cond.add_child(e)
        return cond


    def _standardize_equal(self, node):
        eq = STNode(STNodeType.EQ)
        eq.add_child(node.children[0])
        eq.add_child(node.children[1])
        return eq
    
    def _standardize_operator(self, node):
        op_name = node.node_type.name.lower()
        
        if node.node_type in [NodeType.not_, NodeType.neg]:
            
            OP=(STNode(STNodeType.OP, value=op_name))  
            OP.add_child(node.children[0])
            return OP
        else:
            OP = STNode(STNodeType.OP, value=op_name)  
            OP.add_child(node.children[0])
            OP.add_child(node.children[1])
            return OP
        
    def _standardize_let(self, node):
        gamma = STNode(STNodeType.GAMMA)
        lam = STNode(STNodeType.LAMBDA)
        lam.add_child(node.children[0].children[0])
        lam.add_child(node.children[1])              
        gamma.add_child(lam)
        gamma.add_child(node.children[0].children[1])
        return gamma

    def _standardize_terminal(self, node):
        if node.node_type == NodeType.identifier:
            return STNode(STNodeType.ID, value=f"<ID:{node.value}>")
        elif node.node_type == NodeType.integer:
            return STNode(STNodeType.INT, value=f"<INT:{node.value}>")
        elif node.node_type == NodeType.string:
            return STNode(STNodeType.STR, value=f"<STR:{node.value}>")
