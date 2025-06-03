from Automata.Node import *

#esta parte es el arbol que ya teníamos en TC
# esto era para el afn
def construirArbol(e):
    stack = []
    operators = {"|": 2, ".": 2, "*": 1, "+": 1}

    for c in e:
        if c not in operators:
            node = Node(c)
            stack.append(node)
        else:
            if operators[c] == 2:
                right_operand = stack.pop()
                try:
                    left_operand = stack.pop()
                except IndexError:
                    node = Node(c)
                    node.left = None
                    node.right = right_operand
                    stack.append(node)
                    continue

                node = Node(c)
                node.right = right_operand
                node.left = left_operand
                stack.append(node)

            else:
                operand = stack.pop()
                node = Node(c)
                node.left = operand
                node.right = None
                stack.append(node)

    return stack.pop()
