import networkx as nx  # Librairie pour les graphes
import numpy as np
from utils import *

fixed_points = [1,2]

#  Récupérer les points à modifier
graphe = load_polyfile(filename)
editable_vertices = graphe.copy()
editable_vertices.remove_nodes_from(fixed_points)

# Créer un nouveau graphe avec les points à modifier
subgraph = graphe.subgraph(editable_vertices)

# Calculer delta
L = get_L(subgraph).todense()
V = np.matrix([subgraph.nodes[i]['pos'] for i in subgraph.nodes])
Delta = L.dot(V)

# Créer le système linéaire
n = L.shape[0]
for vertice in subgraph.nodes:
    # Calculer A
    neighbours = subgraph.adj(vertice)
    nb_vertices = len(neighbours) + 1  # +1 is here because we count also the current vertices
    A = np.zeros([nb_vertices * 3, 7])
    vertices_for_A = [vertice] + neighbours

    for j, v in enumerate(vertices_for_A):
        vj_x = v[0]
        vj_y = v[1]
        vj_z = 0
        