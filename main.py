from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *
from AutomatonBuilder.ConstruirAutomata import *
from AutomatonBuilder.grafico import *
from LRParsingAlgorithm.LRParsingAlgorithm import *

from LRParsingAlgorithm.TablaSLR import *


from Yalex.lexicalAnalizer import get_pickle_automata
from Yalex.yalReader import yalReader
from Yalex.generator import generar_afd_unificado, _serialize_automata
from Yalex.constructor_yalex import leerArchivo_yalex
def simular_texto(texto: str, automata) -> List[List[str]]:
    resultados = []
    i = 0

    while i < len(texto):
        estado_actual = automata.afd.estado_inicial
        j = i
        ultimo_estado_final = None
        ultima_pos_final = i
        token_encontrado = None

        while j < len(texto):
            c = texto[j]
            transiciones = automata.afd.transiciones.get(estado_actual, {})
            if c in transiciones:
                estado_actual = transiciones[c]
                j += 1
                if estado_actual in automata.afd.estados_finales:
                    ultimo_estado_final = estado_actual
                    ultima_pos_final = j
                    token_encontrado = automata.estado_a_token.get(estado_actual)
            else:
                break

        if ultimo_estado_final is not None:
            lexema = texto[i:ultima_pos_final]
            resultados.append([lexema, token_encontrado])
            i = ultima_pos_final
        else:
            resultados.append([texto[i], "ERROR"])
            i += 1

    return resultados


def main():


    opi = int(input(("1) Cargar Pickle \n2) Leer yal nuevo\n")))
    lexical_automata = None
    if opi == 1:
        #  lectura del lexical automata
        lexical_automata = get_pickle_automata("./Yalex/out/lexical_out/lexicalAutomata.pkl")
        if lexical_automata:
            pass
        else:
            print("No se pudo encontrar el archivo")
    else:

        contenido_yal = leerArchivo_yalex("yalDocs/slr-4.yal")
        if contenido_yal:
            print(f"\nArchivo Yal leído correctamente\n")

            yal = yalReader(contenido_yal)
            tokens = yal.get_tokens()

            print("Tokens detectados:")
            for nombre, expr in tokens.items():
                print(f"  {nombre}: {expr}")


            lexical_automata = generar_afd_unificado(tokens)
            _serialize_automata(lexical_automata, "lexical_out")

    # agregar validacion de archivo y que sean varios xd
    archivo = "./yapar/slr-2.yalp"
    tokens, producciones = leerYapar(archivo)


    # termina lectura de tokens
    print("\n==== TOKENS ====")
    print(tokens)

    no_terminales = list(producciones.keys())
    terminales = sorted(set(tokens))  #tokens que no son terminales

    #---grammar procesor--
    # calcularFirst
    first = First(producciones)

    # calcularFollow
    follow = calcularFollow(producciones, first)
    print(follow)

    #-- automaton builder--
    # automata LR(0)
    estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado = ConstruirAutomata(producciones) 
    graficar_automata(estados, transiciones, estados_id, estado_aceptacion)

    #-- LR-Parsing Algorithm--

    # 1. tabla slr
    action, goto = TablaSLR(producciones, no_terminales, estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado, follow)

    if estado_aceptacion:
        if '$' not in terminales: 
            terminales.append('$')

    print("\n==================== Tabla SLR (Action | goto) ============================")
    imprimirTablas(action, goto, terminales, no_terminales)

    t = "15+69 -42;"
    tokenizado_tx = simular_texto(t, lexical_automata)
    tokenizado = [elem[1] for elem in tokenizado_tx]
    print(tokenizado)

    tokens_prueba_yalp1 = ["ID", "PLUS", "ID", "TIMES", "LPAREN", "ID", "PLUS", "ID", "RPAREN"]

    resultado = ejecutarParser(tokenizado, action, goto, producciones)

    print(f"\n Resultado del análisis: {'-----ACEPTEADA-----' if resultado else '-----RECHAZADA-----'}")




main()


