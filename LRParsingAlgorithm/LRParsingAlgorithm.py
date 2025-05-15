"""
-- LR-Parsing Algorithm--

tomar de entrada el conjunto canonico de items LR0
y se va a transformar en una estructura de datos, para simular el algoritmo de parsing
se usa una pila para simular el automata de pila
va a consumir token tras token 
consume token tras token y usa la pila y consulta la table slr para determinar la accion que debe de tomar el analizador
la tabla slr accion|goto
la salida es si: si la secuencia de tokens que tenemos en la entrada construye una oracion valida a partir de de la gramatica libre de contexto
la salida es no: si tenemos errores sintacticos, es cuando la tabla slr no se capaz de decirnos que hacer
#al tener la tabla slr, se usa el algoritmo de LR parsing program y alli es cuando me dice si la oracion que estoy parseando es valida o no

Algoritmo de LR parsing program

let a be the first symbol of w$;
while (1){ /*repeat forever*/
    let s be the state on top of the stack;
    if (ACTION[s,a] == shift t) {
        push t onto the stack;
        let a be the next input symbol;
    }else if (ACTION[s,a] = reduce A -> β){
        pop |β| symbols off the stack;
        let state t now be on top of the stackl
        push GOTO[t,A] onto the stack;
        output the production A -> β;
    
    }else if (ACTION[s,a] == accept) break; /* parsing is done*/
    else call error-recovery routine;
    
}

"""





