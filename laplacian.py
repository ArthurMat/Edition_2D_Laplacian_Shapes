import networkx as nx  # Librairie pour les graphes
import numpy as np
from utils import *

def N(graphe, edge):
    v1, v2 = edge
    liste = [v1, v2]
    for neighbour in graphe.adj(v1):
        if neighbour in graphe.adj(v2):
            liste.append(neighbour)
            if len(liste) == 4:
                return liste

handles = [1, 2]

#  Récupérer les points à modifier
graphe = load_polyfile(filename)

# Créer un nouveau graphe avec les points à modifier
new_graph = graphe.subgraph(graphe.nodes)



for k, edge in enumerate(new_graph.edges):
    # Calcul Gk
    vertices = N(graphe, edge)
    Gk_list = []
    for vertice in vertices:
        vx = vertice['pos'](0)
        vy = vertice['pos'](1)

        Gk_list.append(vx)
        Gk_list.append(vy)
        Gk_list.append(vy)
        Gk_list.append(-vx)

    Gk = np.array(Gk_list).reshape((8, 2))

    # Calcul ek
    vi, vj = np.array(edge[0]), np.array(edge[1])
    ek = vj - vi
    ekx, eky = ek[0], ek[1]
    ek_matrix = np.array([ekx, eky, eky, -ekx]).reshape((2, 2))

