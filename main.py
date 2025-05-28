from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *
from AutomatonBuilder.ConstruirAutomata import *
from AutomatonBuilder.grafico import *
from LRParsingAlgorithm.LRParsingAlgorithm import *
from LRParsingAlgorithm.TablaSLR import *


def main():

    #agregar validacion de archivo y que sean varios xd
    archivo = "./yapar/slr-1.yalp"
    tokens, producciones = leerYapar(archivo)

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

    #2. LR Parsing Program
    print("\n==== Prueba de Parsing ====")
    # Solo se pueden usar PLUS y TIMES, con ( ) y solo ID
    # ['ID', 'LPAREN', 'PLUS', 'RPAREN', 'TIMES']
    tokens_prueba_yalp1 = ["ID", "PLUS", "ID", "TIMES", "LPAREN", "ID", "PLUS", "ID", "RPAREN"]
    # Se pueden usar NUMBER, MINUS y DIV ademas de los anteriores
    # ['DIV', 'ID', 'LPAREN', 'MINUS', 'NUMBER', 'PLUS', 'RPAREN', 'TIMES']
    tokens_prueba_yalp2 = ["ID", "PLUS", "NUMBER", "DIV", "LPAREN", "NUMBER", "MINUS", "NUMBER", "RPAREN"]
    # solo PLUS y TIMES y ( ) pero con number en minuscula y sin ID
    # ['LPAREN', 'NUMBER', 'PLUS', 'RPAREN', 'TIMES']
    tokens_prueba_yalp3 = ["number", "PLUS", "LPAREN", "number" , "TIMES", "number", "RPAREN"]
    # Creo que tiene que ser asignaciones nada mas, como A = 3 + (4 * 5) o cosas asi
    # ['ASSIGNOP', 'DIV', 'EQ', 'ID', 'LPAREN', 'LT', 'MINUS', 'NUMBER', 'PLUS', 'RPAREN', 'SEMICOLON', 'TIMES']
    tokens_prueba_yalp4 = [ "ID", "ASSIGNOP", "NUMBER", "PLUS", "NUMBER", "TIMES", "LPAREN", "NUMBER", "MINUS", "NUMBER", "RPAREN"]

    
    resultado = ejecutarParser(tokens_prueba_yalp1, action, goto, producciones)

    print(f"\n Resultado del análisis: {'-----ACEPTEADA-----' if resultado else '-----RECHAZADA-----'}")

main()
