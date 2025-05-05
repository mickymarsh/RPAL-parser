from node import Node  # <-- This is the import line

class TreeBuilder:
    def __init__(self):
        self.stack = []

    def build_tree(self, label, number_of_children):
        children = []
        for i in range(number_of_children):
            child = self.stack.pop()
            children.append(child)
        children.reverse()
        new_node = Node(label, children)
        self.stack.append(new_node)

    def tree_to_string(self, node):
        if not node.children:
            return node.label
        else:
            child_strings = []
            for child in node.children:
                child_str = self.tree_to_string(child)
                child_strings.append(child_str)
            joined = ", ".join(child_strings)
            result = node.label + "(" + joined + ")"
            return result

    def print_tree(self):
        for node in self.stack:
            print(node)