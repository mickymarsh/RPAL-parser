# main.py

from build_ast import TreeBuilder
from node import Node  

builder = TreeBuilder()

builder.stack.append(Node('id1'))
builder.stack.append(Node('id2'))
builder.stack.append(Node('id3'))
builder.build_tree('+', 2)
builder.stack.append(Node('id4'))
builder.build_tree('*', 2)
builder.build_tree('assign', 2)
builder.build_tree('block', 1)

builder.print_tree()

tree_string = builder.tree_to_string(builder.stack[-1])
print("Tree as string:")
print(tree_string)
