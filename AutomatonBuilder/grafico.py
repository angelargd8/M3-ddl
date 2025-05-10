from graphviz import Digraph

def graficar_automata(estados, transiciones, estados_id):
    dot = Digraph(comment="Automata LR(0)")

    # Crear nodos de estados con sus items
    for i, estado in enumerate(estados):
        label = f"I{i}:\n"
        for nt, cuerpo, punto in sorted(estado):
            antes = " ".join(cuerpo[:punto])
            despues = " ".join(cuerpo[punto:])
            label += f"{nt} → {antes} • {despues}\n"
        dot.node(f"I{i}", label=label, shape="box", fontname="Courier")

    # Crear transiciones
    for (origen_id, simbolo), destino_id in transiciones.items():
        origen_label = f"I{estados_id[origen_id]}"
        destino_label = f"I{estados_id[destino_id]}"
        dot.edge(origen_label, destino_label, label=simbolo)

    # Guardar y mostrar
    dot.render("automata_LR0", format="png", cleanup=True)
    print("Automata LR(0) generado como 'automata_LR0.png'")
