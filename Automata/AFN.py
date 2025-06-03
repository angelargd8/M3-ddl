import logging
from Automata.estado import Estado
from typing import List, Set


class Afn:
    def __init__(self):
        self.inicio: Estado = None
        self.final: Estado = None
        self.estados: List[Estado] = []
        self.logger = logging.getLogger(__name__)

    def crearNodo(self) -> Estado:
        estado = Estado(len(self.estados))
        self.estados.append(estado)
        return estado

    def agregar_transicion(self, origen: Estado, simbolo: str, destino: Estado):
        if not isinstance(destino, Estado):
            raise ValueError(
                f"Error: el destino {destino} debería ser una instancia de Estado."
            )
        origen.transiciones.append((simbolo, destino))

    def get_estados(self) -> List[Estado]:
        """Devuelve todos los estados del AFN."""
        return self.estados

    def log_info(self):
        """Registra información del AFN en los logs."""
        self.logger.info("===== Información del AFN =====")
        self.logger.info(
            f"Estado inicial: {self.inicio.number if self.inicio else None}"
        )
        self.logger.info(f"Estado final: {self.final.number if self.final else None}")
        for estado in self.estados:
            self.logger.info(
                f"Estado {estado.number}, Transiciones: {[(s, d.number) for s, d in estado.transiciones]}"
            )
        self.logger.info("================================")
