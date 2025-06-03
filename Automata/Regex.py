from Automata.metachar import Metachar
from collections import deque



def InsertConcatenation(regex: str) -> list:
    if not regex:
        return "ε"
    
    regexProcesada = []
    i = 0

    while i < len(regex):

        #si hay un arroba
        # if regex[i] == '@':
        #     j = i + 1
        #     marcador = '@'
        #     while j < len(regex):
        #         marcador += regex[j]
        #         if regex[j] == '@':
        #             regexProcesada.append(marcador)
        #             i = j + 1
        #             break
        #         j += 1
        #     else:
        #         # Si no se cierra el marcador correctamente, lo tratamos como caracteres sueltos
        #         regexProcesada.append('@')
        #         i += 1
        #     continue

        # Manejar marcadores del tipo #0, #1, etc.
        if regex[i] == '#' and i + 1 < len(regex) and regex[i+1].isdigit():
            j = i + 1
            marcador = '#'
            while j < len(regex) and regex[j].isdigit():
                marcador += regex[j]
                j += 1
            regexProcesada.append(marcador)
            i = j
            continue


        #si hay un caracter escapado
        if i < len(regex) - 1 and Metachar.IsEscaped(regex[i]):
            regexProcesada.append(f"\\{regex[i+1]}") #le puse 2, por como maneja python los escaspados, entonces al recibir el arbol ya tiene \\
            i += 2
            continue
        #literales entre comillas
        elif i < len(regex) - 1 and Metachar.IsQuoted(regex[i]):
            regexProcesada.append(f"{regex[i]}{regex[i+1]}{regex[i+2]}")
            i += 3
            continue
        else: 
            regexProcesada.append(regex[i])
            i += 1
            continue

    result = []
    i = 0

    while i < len(regexProcesada) - 1:
        current = regexProcesada[i]
        next_token = regexProcesada[i + 1]

        # print("- CURRENT " + current )
        # print("- NEXT " + next_token )
        # print("//// ///////////")
        result.append(current)

        is_current_escaped = current.startswith('\\') if len(current) > 1 else False
        is_next_escaped = next_token.startswith('\\') if len(next_token) > 1 else False

        # if (current.startswith("@") and current.endswith("@")) or (next_token.startswith("@") and next_token.endswith("@")):
        #     i += 1
        #     result.append('.')
        #     continue

        # Evitar concatenación entre dos operadores unarios (como +?)
        if Metachar.IsUnaryOperator(current) and Metachar.IsUnaryOperator(next_token):
            i += 1
            continue  


        # Reglas normales para concatenar
        if next_token != '.' and current != '.' or next_token != '(' and current != '(':  #and not (Metachar.IsUnaryOperator(current) and Metachar.IsUnaryOperator(next_token)):
            if (
                (not is_current_escaped and current not in ['(', '|'] and
                not Metachar.IsUnaryOperator(current) and
                not is_next_escaped and next_token not in [')', '|', '*', '+', '?']) 
                or
                (not is_current_escaped and current in ['*', '+', '?', ')'] and
                not is_next_escaped and next_token not in [')', '|', '*', '+', '?'])
                ):

                result.append('.')
                # print("actual" + "".join(result))

        i += 1
        continue

    if regexProcesada:
        result.append(regexProcesada[-1])

    print("REGEX PROCESADA: " + str(result))
    print("REGEX PROCESADA: " + "".join(result))
    return result



#algoritmo que convierte una expresion regular compuesta
#por operadores definidos y operandos infiz a una operacion postfiz
#usa colas
#1 stack para almacernar los operadores de forma temporal por medio de su precendencia con lifo
# 2. la output es donde se tendra la expresion regular en postfix, aqui es donde se usa la precedencia de operadores
#
def infixToPostfix(regex: str) -> list:

    if not regex:
        return ["ε"]
    
    if Metachar.IsBinaryOperator(regex[0]):
        regex = "ε" + regex


    #agregar la concatenacion a la expresion regular
    # tokens = list("(((0|1|2|3|4|5|6|7|8|9))+).((((0|1|2|3|4|5|6|7|8|9))+))?.(E.(\+|-)?.(((0|1|2|3|4|5|6|7|8|9))+))?")
    tokens = InsertConcatenation(regex)
    # print("----> REGEX CONCATEANDO: " + str(tokens))

    operatorStack = [] # stack para los operadores
    outputQueue = deque() # cola para la salida

    #convertir la cadena en una lista de tokens
    #  = list(regex)
    # print("tokens:");print(tokens)
   
    i = 0
    #recorrer la lista de tokens
    while i < len(tokens):
        token = tokens[i]
        # print("=========================================== " )
        # print("TOKEN: " + str(token))
        # print("- output queue: "+ str(outputQueue))
        # print("- Operator stack:" +str(operatorStack))

        #verificar si es un operador
        if len(token) == 1 and Metachar.HasPrecedence(token):

            # print("-----PRECEDENCIA: " + str(Metachar.precedence[token]) + "-----")

            if Metachar.precedence[token] == 0: # (
                operatorStack.append(token)
                # i += 1
                # continue

            elif Metachar.precedence[token] == 4: # )


                #saccar los operadores hasta encontrar los parentesis izquierdo
                while operatorStack and Metachar.precedence[operatorStack[-1]] != 0:
                    # print("////OPERADORES ////")
                    outputQueue.append(operatorStack.pop())
        

                    # if Metachar.HasPrecedence(outputQueue[-1]):

                    #     if Metachar.precedence[outputQueue[-1]] == 3 and Metachar.precedence[operatorStack[-1]] == 2:
                    #         print("////OPERADORES QUE NO NECESITAN PUNTO////")
                    #         operatorStack.pop()
                    #     else: 
                    #         print("/////- SACANDO OPERADOR DEL STACK- //////")
                    #         outputQueue.append(operatorStack.pop())
                    # else: 
                    #     outputQueue.append(operatorStack.pop())
                    
                
                if operatorStack and Metachar.precedence[operatorStack[-1]] == 0: 
                    #eliminar el parentesis izquierdo
                    operatorStack.pop() 

            
            elif Metachar.IsUnaryOperator(token): #* + ?
                #agregar el operador al stack
                operatorStack.append(token)
                

            
            
            else: 
                # mientras que hayua un operador en el stack con mayor o igual precendencia
                while (operatorStack and Metachar.precedence[operatorStack[-1]] != 0 and  #que no sea ( y haya operatorStack
                       Metachar.precedence.get(operatorStack[-1], 0) >= Metachar.precedence.get(token, 0)):
                    
                    # sacar el operador del stack y agregarlo a la salida
                    outputQueue.append(operatorStack.pop())
                
                # # #agregar el operador al stack
                operatorStack.append(token)
                
                # i += 1
                # continue
        else:
            # print("-----NO ES UN OPERADOR-----")
            #es un operando o un caracter escapado, se agrega a la salida
            outputQueue.append(token)
        i += 1
        continue

    #sacar los operadores restantes del stack y agregarlos a la salida
    while operatorStack:
        if Metachar.precedence[operatorStack[-1]] == 0: 
            return "error: Parentesis desbalanceados"
        outputQueue.append(operatorStack.pop())

    #agregar el final 
    outputQueue.append('#')
    outputQueue.append('.')


    # result = ''.join(outputQueue)
    # print("RESULTADO: " + result)
    result = list(outputQueue)


    return result