import networkx as nx  # Librairie pour les graphes
import numpy as np
from utils import *

fixed_points = [1,2]
handles = {}

#  Récupérer les points à modifier
graphe = load_polyfile(filename)
editable_vertices = graphe.copy()
editable_vertices.remove_nodes_from(fixed_points)

# Créer un nouveau graphe avec les points à modifier
subgraph = graphe.subgraph(graphe.nodes)

g2l = {}
for n in subgraph.nodes:
    g2l[n] = len(g2l)
l2g = list(subgraph.nodes)
def get_local_neighbor(subgraph, n, l2g, g2l):
    nb = []
    for i in subgraph.neighbors(l2g[n]):
        nb.append(g2l[i])
    return nb

# Calculer delta
L = get_L(subgraph).todense()
V = np.matrix([subgraph.nodes[i]['pos'] for i in subgraph.nodes])
Delta = L.dot(V)

# Créer le système linéaire
n = L.shape[0]

LS = np.zeros([3 * n, 3 * n])
LS[    0:n,     0:n] = (-1) * L
LS[  n:2*n,   n:2*n] = (-1) * L
LS[2*n:3*n, 2*n:3*n] = (-1) * L

for i, vertice in enumerate(subgraph.nodes):
    nb_idx = get_local_neighbor(subgraph, i, l2g, g2l)
    ring = np.array([i] + nb_idx)

    # Calculer A
    neighbours = subgraph.adj(vertice)
    nb_vertices = len(neighbours) + 1  # +1 is here because we count also the current vertices
    A = np.zeros([nb_vertices * 3, 7])
    vertices_for_A = [vertice] + neighbours

    for k, v in enumerate(vertices_for_A):
        vk_x = v[0]
        vk_y = v[1]
        vk_z = 0
        A[k]                     = [vk_x,    0 ,  vk_z, -vk_y, 1, 0, 0]
        A[k * nb_vertices + 1]   = [vk_y, -vk_z,    0 ,  vk_x, 0, 1, 0]
        A[k * nb_vertices + 2]   = [vk_z,  vk_y, -vk_x,    0 , 0, 0, 1]


    # Calculer s et h
    A_T = A.transpose()
    result = np.dot(np.linalg.inv(np.dot(A_T, A)), A_T)
    s = result[0]
    h = result[1:4]

    T = np.vstack([
         Delta[i, 0] * s    - Delta[i, 1] * h[2] + Delta[i, 2] * h[1],
         Delta[i, 0] * h[2] + Delta[i, 1] * s    - Delta[i, 2] * h[0],
        -Delta[i, 0] * h[1] + Delta[i, 1] * h[0] + Delta[i, 2] * s   ,
    ])
        
    LS[        i, np.hstack([ring, ring+n, ring+2*n])] += T[0]
    LS[    i + n, np.hstack([ring, ring+n, ring+2*n])] += T[1]
    LS[i + 2 * n, np.hstack([ring, ring+n, ring+2*n])] += T[2]

#  Ajouter les contraintes au système linéaire
constraint_coef = []
constraint_b = []

#  Contraintes limites
boundary_idx = [g2l[i] for i in fixed_points]
for idx in boundary_idx:
    constraint_coef.append(np.arange(3*n) == idx)
    constraint_coef.append(np.arange(3*n) == idx + n)
    constraint_coef.append(np.arange(3*n) == idx + 2*n)
    constraint_b.append(V[idx, 0])
    constraint_b.append(V[idx, 1])
    constraint_b.append(V[idx, 2])
  
#  Contraintes handles
for gid, pos in handles.items():
    idx = g2l[gid]
    constraint_coef.append(np.arange(3*n) == idx)
    constraint_coef.append(np.arange(3*n) == idx + n)
    constraint_coef.append(np.arange(3*n) == idx + 2*n)
    constraint_b.append(pos[0])
    constraint_b.append(pos[1])
    constraint_b.append(pos[2])
    
constraint_coef = np.matrix(constraint_coef)
constraint_b = np.array(constraint_b)

A = np.vstack([LS, constraint_coef])
b = np.hstack([np.zeros(3*n), constraint_b])
spA = scipy.sparse.coo_matrix(A)

V_prime = scipy.sparse.linalg.lsqr(spA, b)


#  Nouveaux points
new_pnts = []
for i in range(n):
    new_pnts.append([V_prime[0][i], V_prime[0][i+n], V_prime[0][i+2*n]])