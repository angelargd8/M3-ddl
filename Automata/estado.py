from graphviz import Graph


class Estado:
    def __init__(self, number, trans=None):
        self.number = number
        self.transiciones = []  # Lista de transiciones en lugar de hijo1/hijo2
        self.es_final = False  # Indica si el estado es final

    def agregar_transicion(self, simbolo, destino):
        """Agrega una transición a este estado."""
        self.transiciones.append((simbolo, destino))

    def obtener_transiciones(self):
        """Devuelve la lista de transiciones del estado."""
        return self.transiciones

    def __repr__(self):
        return f"Estado({self.number}, final={self.es_final}, transiciones={self.transiciones})"
