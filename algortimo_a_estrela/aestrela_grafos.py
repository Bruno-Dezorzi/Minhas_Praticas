from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt

# Definimos o destino fixo da busca (célula superior esquerda do labirinto)
NO_INICIAL = 'Arad'
NO_DESTINO = 'Bucharest'

EDGES = [
        ("Arad", "Zerind", 75),
        ("Arad", "Timisoara", 118),
        ("Arad", "Sibiu", 140),
        ("Zerind", "Oradea", 71),
        ("Oradea", "Sibiu", 151),
        ("Timisoara", "Lugoj", 111),
        ("Lugoj", "Mehadia", 70),
        ("Mehadia", "Drobeta", 75),
        ("Drobeta", "Craiova", 120),
        ("Craiova", "Rimnicu Vilcea", 146),
        ("Craiova", "Pitesti", 138),
        ("Rimnicu Vilcea", "Sibiu", 80),
        ("Rimnicu Vilcea", "Pitesti", 97),
        ("Sibiu", "Fagaras", 99),
        ("Fagaras", "Bucharest", 211),
        ("Pitesti", "Bucharest", 101),
        ("Bucharest", "Giurgiu", 90),
        ("Bucharest", "Urziceni", 85),
        ("Urziceni", "Hirsova", 98),
        ("Hirsova", "Eforie", 86),
        ("Urziceni", "Vaslui", 142),
        ("Vaslui", "Iasi", 92),
        ("Iasi", "Neamt", 87)
    ]

# --------------------------
# Heurística (straight-line distance aproximada)
# --------------------------
# Coordenadas fictícias (para simular distância aérea entre cidades)
# Obs: aqui usei valores aproximados do mapa de Romenia usado no exemplo clássico.
coords = {
    'Arad': (91, 492),
    'Zerind': (108, 531),
    'Oradea': (120, 571),
    'Timisoara': (75, 445),
    'Lugoj': (165, 379),
    'Mehadia': (168, 339),
    'Drobeta': (191, 299),
    'Craiova': (253, 288),
    'Sibiu': (207, 457),
    'Rimnicu Vilcea': (233, 410),
    'Pitesti': (289, 339),
    'Fagaras': (274, 444),
    'Bucharest': (333, 331),
    'Giurgiu': (334, 249),
    'Urziceni': (410, 257),
    'Hirsova': (465, 270),
    'Eforie': (473, 243),
    'Vaslui': (442, 380),
    'Iasi': (417, 463),
    'Neamt': (406, 537),
}

def h_score(no_atual, no_destino):
    """
    Calcula a distancia do nó(lugar) atual até o final independente de 'barreiras'
    """
    (x1, y1) = coords[no_atual]
    (x2, y2) = coords[no_destino]
    return abs(x1 - x2) + abs(y1 - y2) 


def aestrela(G, inicio, destino):
        """
        Implementação do algoritmo A*
        """

        g_score = {no: float('inf') for no in G.nodes}
        f_score = {no: float('inf') for no in G.nodes}
        
        g_score[inicio] = 0
        f_score[inicio] = g_score[inicio] + h_score(inicio,destino)
        
        fila = PriorityQueue()
        fila.put((f_score[inicio],inicio))
        
        caminho = {inicio: None}

        while not fila.empty():
            prioridade, no_atual = fila.get()

             # Verifica se chegamos ao destino
            if no_atual == destino:
                break

            # Explora vizinhos
            for vizinho in G.neighbors(no_atual):
                peso_aresta = G[no_atual][vizinho]['weight']
                tentativo_g = g_score[no_atual] + peso_aresta

                if tentativo_g < g_score[vizinho]:
                    caminho[vizinho] = no_atual
                    g_score[vizinho] = tentativo_g
                    f_score[vizinho] = tentativo_g + h_score(vizinho, destino)
                    fila.put((f_score[vizinho], vizinho))

        # Reconstrução do caminho
        caminho_final = []
        no = destino
        while no is not None:
            caminho_final.append(no)
            no = caminho.get(no)
        caminho_final.reverse()

        return caminho_final, g_score[destino]

G = nx.Graph()
for u,v,w in EDGES:
    G.add_edge(u,v, weight = w)
    
    
# --------------------------
# Executando o A*
# --------------------------
rota, custo = aestrela(G, NO_INICIAL, NO_DESTINO)
print(f"Melhor caminho de {NO_INICIAL} até {NO_DESTINO}: {rota}")
print(f"Custo total: {custo}")

# --------------------------
# Visualização
# --------------------------
pos = coords  # Usa coordenadas para desenhar

plt.figure(figsize=(10,7))
nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=8)

# Destacar caminho encontrado
path_edges = list(zip(rota, rota[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color="red")
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

plt.title(f"Caminho A*: {NO_INICIAL} → {NO_DESTINO} (custo {custo})")
plt.show()