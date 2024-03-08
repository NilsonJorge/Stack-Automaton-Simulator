def ajusta_transicao(estados,simbolos,transicoes_parciais):
    transicoes = []
    for i in range(len(estados)):
        for j in range(len(simbolos)):
            for k in transicoes_parciais[i][j]:
                if (k != ''):
                    a = k.replace("/", ",").replace("(",'').replace(")",'')
                    b = a.split(",")

                    aux =[]
                    aux.append(estados[i])
                    aux.append(simbolos[j])
                    transicoes.append(aux+b)
    print(transicoes)
    return transicoes

#le o arquivo txt contendo a tabela de transicao de uma PDA
while (True):
    var = input("Informe o nome do arquivo .txt que contem a tabela de transição do PDA. Exemplo(PDA.txt):")
    try:
        with open(var, "r") as arquivo:
            tabela = arquivo.readlines()
        # print(tabela)
        break
    except:
        print("ERRO arquivo nao existe")

# coleta os simbolos
simbolos_arquivo = tabela[0]
simbolos = simbolos_arquivo.split()
print(simbolos)# conjunto de símbolos terminais


#coleta as linhas onde estao as transicoes
linhas = []
for i in range(1, len(tabela)):
    linhas.append( tabela[i].split())
#------------------------------------

verifica_estado = []
for char in linhas:
    verifica_estado.append(char[0])
#coletar o inicial
for estado in verifica_estado:
    if '>' in estado:
        estado_inicial = estado.replace('>','')
        estado_inicial = estado_inicial.replace('*', '')

print("Estado inicial:")
print(estado_inicial)

# Coleta o nome dos estados
estados = []
for char in linhas:
    aux = char[0].replace('>', '')
    aux = aux.replace('*', '')
    estados.append(aux)
    del char[0]
print("Estados do PDA:")
print(estados)



transicoes_parciais = {}
for i in range(len(linhas)):
    # print(linhas[i])
    transicoes_parciais[i] = {}
    for j in range(len(linhas[i])):
        # print(linhas[i][j])
        aux = linhas[i][j].replace('{', '')
        aux = aux.replace('}', '')
        aux = aux.split(';')
        # print(aux)
        transicoes_parciais[i][j] = aux
        for k in range(len(linhas[i][j])):
            # print(linhas[i][j][k])
            aux = linhas[i][j][k].replace('{', '')
            aux = aux.replace('}', '')
            # print(aux)
print("Transacoes")
print(transicoes_parciais)
transicao = ajusta_transicao(estados,simbolos,transicoes_parciais)

#le o arquivo contendo as strings que serao avaliadas
while (True):
    var = input(
        "Informe o nome do arquivo .txt que contem as strings que serão testadas pelo autômato. Exemplo(string.txt):")
    try:
        with open(var, "r") as arquivo:
            dados = arquivo.readlines()
        break
    except:
        print("ERRO arquivo nao existe")

    # coloca as strings do arquivo em uma lista
strings = []
for i in range(len(dados)):
    string = dados[i].split()
    string = list(string[0])
    strings.append(string)
print("Strings para leitura: ")
print(strings)
#-------------------------------------------------------------



# função recursiva para percorrer cada string de entrada
def percorreString(stringAtual, estadoAtual, pilha):
    # pega o símbolo da cadeia atual a ser analisado
    print("Pilha")
    print(pilha)
    print("String atual")
    print(stringAtual)

    if(stringAtual != []):
        simboloAtual = stringAtual[0]

    # cadeias que ja foram totalmente percorridas ou cadeias vazias
    if (stringAtual == [] and pilha == []):
        return True
    elif(stringAtual != [] and pilha == []):
        return False
        # confere se o estado atual é um de aceitação

    # laço for para percorrer todas as possíveis transições
    for i in range(len(transicao)):


        # pega as informações da transição atual

        transicaoAtual = transicao[i]
        estadoInicialT = transicaoAtual[0]#o estado atual para a transicao
        simboloT = transicaoAtual[1]#simbolo terminal daquela transição
        topoPilhaT = transicaoAtual[3]# elemento que deve estar no topo da pilha para essa transicao
        topoPilha = pilha[-1]


        # qualquer cadeia que NÃO tenha sido totalmente percorrida
        if(stringAtual != []):
            # pega o elemento que esta no topo da pilha
            if((estadoInicialT == estadoAtual) and (topoPilhaT == topoPilha)):
                # confere se o símbolo da transição é um símbolo do automato,
                # segue a transição e PERCORRE a cadeia
                if(simboloT == simboloAtual):
                    # define o estado atingido, a cadeia nova e a lista de
                    # cadeia de símbolos a ser empilhada
                    cadeiaNova = stringAtual[1:]#remove o primeiro elemento da cadeia atual, pois o mesmo ja foi testado
                    estadoNovo = transicaoAtual[2]
                    empilha = list(transicaoAtual[4])
                    # função que trata o empilhar da cadeia de símbolos da pilha
                    if(empilhar(cadeiaNova, estadoNovo, pilha, empilha)):
                        return True

        elif(stringAtual == []):#se a string estiver vazia verifica para o simbolo vazio a existencia de alguma transicao adequada
            if((estadoInicialT == estadoAtual) and (simboloT == "&") and (topoPilha ==topoPilhaT) ):
                # define o estado atingido, a string nova e a lista de caracteres ser empilhada
                cadeiaNova = stringAtual
                estadoNovo = transicaoAtual[2]
                empilha = list(transicaoAtual[4])
                # função que trata o empilhar da cadeia de símbolos da pilha
                if(empilhar(cadeiaNova, estadoNovo, pilha, empilha)):
                    return True
    return False


# função para tratar o empilhar da cadeia de símbolos da pilha
def empilhar(stringNova, estadoNovo, pilha, empilha):
    # apenas deleta o topo da pilha
    if(empilha == ['&']):
        popped = pilha.pop()
        if(percorreString(stringNova, estadoNovo, pilha)):
            return True
        else:
            pilha.append(popped)

    elif(empilha != ['&']):
        empilhaReverso = empilha[::-1]#inverte os elementos que seraao empilhados, AB ->BA
        popped = pilha.pop()#remove o elemento que está no topo da pilha,ABAB -> ABA
        pilhaNova = pilha + empilhaReverso#atualiza a pilha, ABABA
        # chama a função principal para continuar percorrendo a string
        if(percorreString(stringNova, estadoNovo, pilhaNova)):
            return True
        # desfaz o que foi feito na pilha caso o caminho não seja válido
        else:
            pilha.append(popped)


# aceitação ou rejeição de cada cadeia de
resultado = []
for j in range(len(strings)):
    pilha = ['Z']# Z é o elemento ques estará no funda da pilha
    stringAtual = strings[j]
    if(percorreString(stringAtual, estado_inicial, pilha)):
        print("aceita")
        aux = ("".join(stringAtual))
        resultado.append(aux + " *\n")
    else:
        print("rejeita")
        aux = ("".join(stringAtual))
        resultado.append(aux + "\n")
try:
    with open("resultado.txt", "w") as arquivo:
        arquivo.writelines(resultado)
except:
    print("ERRO arquivo nao existe")