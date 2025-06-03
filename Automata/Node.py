
class Node:
    
    latest_id = 0

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()

        Node.latest_id += 1
        self.id = Node.latest_id

    # imprimir el arbol en formato grafico
    def printTree(self):
        if self.left:
            self.left.printTree()

        if self.right:
            self.right.printTree()

    # renderizr el arbol y guardarlo en un archivo
    def renderTree(self):
        Node.tree_graph.render("arboles", view=True)

    def displayValue(self):
        if isinstance(self.value, str) and len(self.value) > 1 and self.value.startswith("\\"):
            # Mantener la notación de escape para caracteres especiales
            special_chars = {'t', 'n', 'r', 'v', '\\', '0'}
            if self.value[1] not in special_chars:
                return self.value[1]  #mostrar el caracter de escape
        return self.value


    # esta funcion, nos la dio la IA porque no entontraba un error en el arbol sintactico
    def __str__(self):
        return f"Node(value={self.value}, id={self.id}, nullable={self.nullable}, firstpos={self.firstpos}, lastpos={self.lastpos})"


# la tablita de siguientepos
# en esto tambien nos ayudo la IA para verificar que todo estuviera bien
def calcular_followPos(node, followpos):
    if node is None:
        return

    #procesar los hijos
    calcular_followPos(node.left, followpos)
    calcular_followPos(node.right, followpos)

    #concatenacion
    if node.value == '.':
        for pos in node.left.lastpos:
            if pos not in followpos:
                followpos[pos] = set()
            followpos[pos].update(node.right.firstpos)


    if node.value in ['+', '*']:
        for pos in node.left.lastpos:
            if pos not in followpos:
                followpos[pos] = set()
            followpos[pos].update(node.left.firstpos)

    for pos in node.firstpos.union(node.lastpos):
        if pos not in followpos:
            followpos[pos] = set()
