from pyamaze import maze, agent
from queue import PriorityQueue

# Definimos o destino fixo da busca (célula superior esquerda do labirinto)
destino = (1,1)

def h_score(celula: tuple, destino: tuple):
    """
    Calcula a distancia do nó(lugar) atual até o final independente de 'barreiras'
    """
    xc = celula[0]
    yc = celula[1]
    xd = destino[0]
    yd = destino[1]
    return abs(yc - yd) + abs(xc - xd) 


def aestrela(labirinto):
        """
        Implementação do algoritmo A* para encontrar o melhor caminho
        dentro do labirinto.
        """

        # Inicializa todos os f_score como infinito
        f_score = {celula : float ("inf") for celula in labirinto.grid}

        # g_score guarda a "distância real" percorrida até chegar em uma célula
        g_score = {}

        # Define a célula inicial como a posição inferior direita do labirinto
        celula_inicial = (labirinto.rows, labirinto.cols)

        # Inicializa g_score da célula inicial como 0
        g_score[celula_inicial] = 0

        # Calcula o f_score inicial = g_score + heurística (h_score)
        f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula=celula_inicial, destino=destino)
        
        # Fila de prioridade (min-heap) onde cada item contém:
        # (f_score, h_score, célula)
        fila = PriorityQueue()
        item = (f_score[celula_inicial], h_score(celula=celula_inicial,destino=destino), celula_inicial)
        fila.put(item)
        
        # Dicionário que guarda "de onde viemos" para reconstruir o caminho depois
        caminho = {}
        
        # Enquanto houver células na fila de prioridade
        while not fila.empty():
            # Retira a célula com menor f_score
            celula = fila.get()[2]
            
            # Se chegamos ao destino, encerramos a busca
            if celula == destino:
                break
            
            # Explora os vizinhos em cada direção (Norte, Sul, Oeste, Leste)
            for direcao in "NSEW":
                # Verifica se existe passagem na direção escolhida (sem parede)
                if labirinto.maze_map[celula][direcao] == 1:
                    linha_celula = celula[0]
                    coluna_celula = celula[1]

                    # Determina qual é a próxima célula, dependendo da direção
                    if direcao == "N":
                        proxima_celula = (linha_celula - 1, coluna_celula)
                    elif direcao == "S":
                        proxima_celula = (linha_celula + 1, coluna_celula)
                    elif direcao == "W":
                        proxima_celula = (linha_celula, coluna_celula - 1) 
                    elif direcao == "E":
                        proxima_celula = (linha_celula, coluna_celula + 1)
                        
                    # Calcula novo custo do caminho até a próxima célula
                    novo_g_score = g_score[celula] + 1
                    novo_f_score = novo_g_score + h_score(proxima_celula, destino)
                    
                    # Se encontramos um caminho melhor (menor f_score), atualizamos
                    if novo_f_score < f_score[proxima_celula]:
                        f_score[proxima_celula] = novo_f_score
                        g_score[proxima_celula] = novo_g_score
                        item = (novo_f_score, h_score(proxima_celula,destino), proxima_celula)
                        fila.put(item)
                        caminho[proxima_celula] = celula
                        
        # Reconstrução do caminho final percorrido:
        # a partir do destino, voltamos pelas células até a inicial
        caminho_final = {}
        celula_analisa = destino
        while celula_analisa != celula_inicial:
            caminho_final[caminho[celula_analisa]] = celula_analisa
            celula_analisa = caminho[celula_analisa]
        
        return caminho_final


# Cria um labirinto 
labirinto = maze(100,100)
labirinto.CreateMaze()

# Cria um agente que vai percorrer o labirinto
agente = agent(labirinto, filled=True, footprints=True)

# Executa o algoritmo A* e obtém o caminho encontrado
caminho = aestrela(labirinto)

# Desenha o caminho encontrado no labirinto
labirinto.tracePath({agente: caminho}, delay = 10)

# Executa a simulação
labirinto.run()
