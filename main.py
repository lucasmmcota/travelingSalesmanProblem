import time


def preencheMatrizAdjacencia(matriz, matAdj):
    for i in matriz[0]:
        separador = i.split()

        v1 = (int(separador[0]))
        v2 = (int(separador[1]))
        peso = (float(separador[2]))

        matAdj[v1][v2] = peso
        matAdj[v2][v1] = peso
    return matAdj


def escreverArquivoSaida(C, indice):
    arquivo = open("saida.txt", 'w')

    string = [[] for i in range(len(C) + 2)]
    string[0] = " " + str(custo[indice]) + "\n"
    for i in range(len(C)):
        string[i+1] = str(C[i][0]) + " "
    string[len(C) + 1] = str(C[0][0])

    for i in string:
        arquivo.write(i)

    arquivo.close()


def vizinhoMaisProximo(G, tempo, indice):
    inicio = time.time()

    u = 0   # Vértice atual
    C = []  # Caminho final
    Q = [i for i in range(len(G))]  # Lista de vértices a serem processados
    Q.remove(u)
    custo[indice] = 0

    while len(Q) != 0:  # Enquanto houver vértices a serem processados
        min = float("inf")
        v = -1

        for i in Q:     # Procura pelo vizinho mais próximo
            if min > G[u][i] and G[u][i] != 0:
                min = G[u][i]
                v = i
        if v == -1:
            print("\nNão foi possível concluir um caminho com este nivel de refinamento !")
            return []

        custo[indice] += min
        
        C.append((u, v))    # Adiciona o caminho do vizinho mais próxima a lista
        Q.remove(v)         # Remove o vértice dos vértices não processados
        u = v               # Atualiza para o próximo vértice

        aux = time.time()
        if (aux - inicio) > tempo:
            print("\nNão foi possível achar a rota pelo método do Vizinho Mais Próximo no limite de tempo estabelecido !")
            return []

    custo[indice] += G[u][0]
    C.append((u, 0))    # Adiciona o ultimo vértice para fechar o ciclo
    fim = time.time()

    tempoExecucao[indice] = fim - inicio    # Tempo de execução do algoritmo

    return C    # Retorna o caminho percorrido


def refinamento_k_opt(G, tempo, opt):
    C = vizinhoMaisProximo(G, tempo, 0)

    tamanhoCaminho = [[] for i in range(len(C))]
    arestasExcluidas = [[] for i in range(opt)]

    j = 0

    for i in C:
        tamanhoCaminho[j] = G[i[0]][i[1]]   # Pesos do caminho percorrido
        j += 1

    for i in range(opt):
        arestasExcluidas[i] = max(tamanhoCaminho)
        indice = tamanhoCaminho.index(max(tamanhoCaminho))   # Indice do maior caminho percorrido
        tamanhoCaminho[indice] = float('-inf') # O maior caminho recebe o valor "-infinito"
        G[C[indice][0]][C[indice][1]] = 0   # As arestas excluidas recebem 0
        G[C[indice][1]][C[indice][0]] = 0

    C2 = vizinhoMaisProximo(G, tempo, 1)
    if custo[1] > custo[0] or not C2:
        print("\nO caminho sem refinamento tem um custo menor !")
        print("Custo: {:.2f}". format(custo[0]))
        print("Tempo:", tempoExecucao[0], "s\n")
        escreverArquivoSaida(C, 0)
    else:
        print("\nO caminho com refinamento tem um custo menor !")
        print("Arestas excluidas:", arestasExcluidas)
        print("Custo: {:.2f}". format(custo[1]))
        print("Tempo:", tempoExecucao[1], "s\n")
        escreverArquivoSaida(C2, 1)


nomeArquivo = input("\nInforme o grafo: ")
arquivo = open(nomeArquivo, 'r')

cabecalho = arquivo.readline()
cabecalho = cabecalho.split()
numVertices = int(cabecalho[0])
numArestas = float(cabecalho[1])

matriz = []
matriz.append(arquivo.readlines())
matAdj = [[0 for i in range(numVertices)]for i in range(numVertices)]
matAdj = preencheMatrizAdjacencia(matriz, matAdj)

tempo = int(input("Tempo limite (s): "))
opt = int(input("Digite o nivel de refinamento: "))

custo = [[] for i in range(2)]
tempoExecucao = [[] for i in range(2)]

refinamento_k_opt(matAdj, tempo, opt)

arquivo.close()
