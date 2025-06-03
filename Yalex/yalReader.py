

# parseo del yalex
class yalReader:
    def __init__(self, text):
        self.text = text
        self.list = [] # para llevar el orden / es necesario cuidar la precedencia
        self.dicc = {}  # diccionario para las definiciones y expresiones

        self.rules_tokens = {}
        self.tokens = {}

        self.header = ""
        self.trailer = ""

        self.simbols = "+*|()[]?'#."
        self.operators = "+*?"

        # mandar a llamar funciones
        self.remove_comments()
        self.read_yalex()
        self.parse()
        self.parse_tokens()
        print(self.tokens)


    def get_rules_tokens(self):
        return self.rules_tokens

    def get_tokens(self):
        return self.tokens

    def get_header(self):
        return self.header

    def get_trailer(self):
        return self.trailer

    def expand_optional(self,expression) :
        new_exp = ""
        stack = []  # Pila para rastrear los índices de paréntesis abiertos
        i = 0

        while i < len(expression):
            # if expression[i] == "?":
            #     print("")
            #     # if stack:
            #     #     # Último paréntesis abierto
            #     #     start = stack.pop()
            #     #     substr = new_exp[start:]  # Extraer contenido desde el paréntesis
            #     #     new_exp = new_exp[:start] + f"(ε|{substr})"
            #     # else:
            #     #     # Si no hay paréntesis, tomar el último carácter como afectado
            #     #     new_exp = new_exp[:-1] + f"(ε|{new_exp[-1]})"
            #     # i += 1  # Saltar el '?'
            if expression[i] == ")":
                # Extraer el contenido del grupo
                start = stack.pop()
                stack.append(start)  # Guardar de nuevo para posible `?`
                new_exp += expression[i]
                i += 1
            elif expression[i] == "(":
                # Guardar la posición del paréntesis abierto
                stack.append(len(new_exp))
                new_exp += expression[i]
                i += 1
            else:
                new_exp += expression[i]
                i += 1

        return new_exp


    # diccionario de los tokens en regex para generacion posterior de afds
    def parse_tokens(self):
        for key in self.rules_tokens:
            if key in self.dicc: # remplaza los regex ya creados
                remplazo = self.dicc[key]
                # Reemplazo explícito de secuencias como \\n -> \n, \\t -> \t
                remplazo = remplazo.replace("\\n", "\n").replace("\\t", "\t").replace("\\s", " ")

                self.tokens[self.rules_tokens[key]] = remplazo
            else: # si no es regex jalar solo el valor que tiene
                key = key.strip()
                print(key)
                if key[0] == "\"":
                    j = 1
                    temp = ""
                    while j < len(key) and key[j] != "\"":
                        if key[j] in self.simbols:
                            temp += "\\" + key[1]
                        else:
                            temp += key[j]
                        j += 1
                    temp = temp.replace("\\n", "\n").replace("\\t", "\t").replace("\\s", " ")

                    self.tokens[self.rules_tokens[key]] = temp
                else:
                    if key[1] in self.simbols:
                        self.tokens[self.rules_tokens[key]] = "\\"+key[1]
                    else:
                        self.tokens[self.rules_tokens[key]] = key[1]


    # en el caso de expresiones como [a-z] nos apoyamos del orden ascii y de las funciones de ord y chr
    # parsea las expresiones regulares a algo que podamos reconocer
    def parse(self):
        for n in self.list:
            expresion = self.dicc[n]
            i = 0
            new_exp = ""
            while i < len(expresion):
                temps = ""
                if expresion[i] == "[": # significa que es una expresión regular y hay que parsearla
                    cadena = True
                    # new_exp += "("
                    while cadena:
                        i += 1

                        if expresion[i] == "'": # si empieza con comillas simples cada caracter está en comillas simples y se debe de separar por ellas
                            if expresion[i+1] in self.simbols: # esto sirve para validar los simbolos que están dentro de comillas
                                temps += "(\\"+expresion[i + 1]+")"
                                i += 4
                                temps += "|"
                            else:
                                temps += expresion[i+1]
                                i += 2

                            while expresion[i] != "'":
                                temps += expresion[i]
                                i += 1

                            if expresion[i+1] == "-": # expresiones que sean de 'a'-'z'
                                temps2 = self.get_ascii(expresion[i-1], expresion[i+3])
                                # print("Q!!!!!!! ", temps)
                                if temps2 != "":
                                    temps += "|" + temps2
                                i += 4 # se salta hasta la siguiente expresion porque ya validó el rango
                            if i+2 < len(expresion) and expresion[i+1] != "]":
                                temps += "|"
                        if expresion[i] == "\"": # si la expresion empieza con " comillas dobles, significa que la separacion es diferente
                            i += 1
                            while expresion[i] != "\"":
                                if expresion[i] in self.simbols: # la expresion tiene que ir en escapado
                                    temps += "(\\"+expresion[i]+")"
                                else:
                                    if expresion[i] == "\\":
                                        temps += "("+expresion[i] + expresion[i+1]+")"
                                        # print("!!!!!!!!"+temps)
                                        i += 1
                                    else:
                                        temps += expresion[i]
                                i += 1
                                if i + 2 < len(expresion):
                                    temps += "|"

                        if expresion[i] == "]": # termina la cadena dentro de []
                            cadena = False
                            grouped = "(" + temps + ")"
                            if i + 1 < len(expresion) and expresion[i + 1] in self.simbols:
                                new_exp += grouped + expresion[i + 1]
                                i += 1
                            else:
                                new_exp += grouped
                            i += 1

                else: # significa que hace referencia a otra variable y hay que remplazarla
                    if expresion[i] in self.simbols :
                        if expresion[i] == "'":
                            i += 1 # me salto la primera '
                            if expresion[i] in self.simbols:
                                new_exp += "(\\"+expresion[i]+")" # agrego \ y la letra
                                # print("!!!!!!!!!!!!!!!!!!!!!!"+ new_exp)
                            else:
                                new_exp +=  expresion[i]
                            i += 2 # me salto la letra y la otra '
                        else:
                            new_exp += expresion[i]
                            i += 1
                    else:
                    # leemos letra por letra hasta encontrar un simbolo
                        # se guarda en un temp para evaluar si existe en el diccionario
                        # si existen se remplaza por el valor que ya tenia
                        temp = ""
                        while i < len(expresion) and expresion[i] not in self.simbols and expresion[i] != '.':
                            temp += expresion[i]
                            i += 1
                        reemplazo = "(" + self.dicc[temp] + ")"
                        if i < len(expresion) and expresion[i] in self.simbols:
                            # Si lo siguiente es un '?', entonces agrupa TODO lo anterior
                            if i + 1 < len(expresion) and expresion[i + 1] == "?":
                                new_exp += "(" + reemplazo + expresion[i] + ")?"  # todo el grupo opcional
                                i += 2
                            else:
                                new_exp += reemplazo + expresion[i]
                                i += 1
                        else:
                            new_exp += reemplazo
                            if i < len(expresion) and expresion[i] == "?":
                                new_exp = "(" + new_exp + ")?"
                                i += 1

            print(new_exp)
            # new_exp = new_exp.replace(".", "\.")
            self.dicc[n] = new_exp # se remplaza la expresion ya formateada en regex para su uso mas adelante


    # lee el archivo para colocarlo en los diccionarios y
    def read_yalex(self):
        self.remove_comments()
        i = 0
        inside_rules = False
        is_header = True
        length = len(self.text)

        while i < length:
            if self.text[i:i + 4] == "let ":
                i += 4  # Avanzamos después de "let "

                # Obtener nombre de la variable
                # sabemos que despues de let viene inmediatamente el nombre de la variable
                nombre = ""
                while i < len(self.text) and self.text[i].isalnum():
                    nombre += self.text[i]
                    i += 1

                # Saltar espacios en blanco y encontrar el '='
                while i < len(self.text) and self.text[i] in " \t":
                    i += 1

                if i < len(self.text) and self.text[i] == "=":
                    i += 1  # Saltar '='

                # Obtener valor (hasta encontrar un salto de línea que no esté dentro de [])
                # También lee lo que no este dentro de [] y termina cuando encuentra \n
                valor = ""
                dentro_corchetes = False
                while i < len(self.text):
                    if self.text[i] == "[":
                        dentro_corchetes = True
                    elif self.text[i] == "]":
                        dentro_corchetes = False
                    elif self.text[i] == "\n" and not dentro_corchetes:
                        break  # Fin del valor

                    valor += self.text[i]
                    i += 1

                self.list.append(nombre.strip()) # agrega el nombre a la lista para saber el orden en el que aparecieron
                self.dicc[nombre.strip()] = valor.strip() # agrega el nombre y expresión al diccionario


            # headers
            if self.text[i] == "{" and not inside_rules:
                i += 1 # saltarse {
                temp = ""
                while i < length and self.text[i] != "}":
                    temp += self.text[i]
                    i += 1
                if is_header:
                    self.header += temp
                else:
                    self.trailer += temp
                is_header = False
                i += 1 # saltarse }

            # rules tokens
            # Detectar inicio de rule tokens
            if self.text[i:i + 13] == "rule tokens =":
                inside_rules = True
                i += 13

            if inside_rules:

                while i < length and self.text[i].isspace():
                    i += 1
                # Reconocer el primero

                # Leer patrón del token
                if self.text[i] == '|':
                    i += 1

                while i < length and self.text[i].isspace():
                    i += 1

                pattern = ""
                while i < length and self.text[i] not in "{\n":
                    pattern += self.text[i]
                    i += 1
                pattern = pattern.strip()

                # Leer nombre del token
                token_name = ""
                while i < length and self.text[i] != '{':
                    i += 1
                i += 1  # Saltar '{'

                while i < length and self.text[i].isspace():
                    i += 1

                if self.text[i:i + 6] == "return":
                    i += 6
                    while i < length and self.text[i].isspace():
                        i += 1

                    while i < length and self.text[i] != '}':
                        token_name += self.text[i]
                        i += 1
                    i += 1
                token_name = token_name.strip()
                if pattern and token_name:
                    self.rules_tokens[pattern] = token_name

                if i < length:
                    while self.text[i].isspace():
                        i += 1

                    if self.text[i] != "|": # si lo siguiente que encuentra ya no es un or despues
                        inside_rules = False
                        if self.text[i]== "{":
                            i -= 1


            i += 1  # Avanzar en el código

        return True # para el módulo de pruebas

    # elimina los comentarios del texto
    def remove_comments(self):
        result = []
        i = 0
        inside_comment = False

        while i < len(self.text):
            if self.text[i:i + 2] == "(*":
                inside_comment = True
                i += 2  # Saltar el inicio del comentario
            elif self.text[i:i + 2] == "*)" and inside_comment:
                inside_comment = False
                i += 2  # Saltar el final del comentario
            elif not inside_comment:
                result.append(self.text[i])
                i += 1
            else:
                i += 1  # Ignorar caracteres dentro del comentario

        # sustituye el texto ya sin los comentarios, strip quita los espacios
        self.text = "".join(result).strip()
        return self.text


    # regresar el rango de caracteres con ayuda de ascii
    # regresa toda la expresión a excepción del primero
    def get_ascii(self, inicio, fin)-> str:
        return '|'.join(chr(i) for i in range(ord(inicio) + 1, ord(fin) + 1))
