# Edition_2D_Laplacian_Shapes
Le but de ce projet est de développer un outil de déformation de surfaces de type "Edition par Laplacien". Ces méthodes de déformations fonctionnent suivant la "handle metaphor", i.e. pour un maillage donné il faut choisir 2 types de contraintes pour la déformation: (1) un handle (une "poignée") est généralement un ensemble de sommets que l’utilisateur déplace de facon rigide et qui guide la déformation du maillage. (2) les contraintes fixes sont un ensemble de sommets (minimum 1 sommet) qui ne bougent pas lors de la déformation. Le maillage déformée est ensuite calculé en minimisant une fonction d’énergie quadratique (un Laplacien par exemple) sous contraintes, ce qui revient à résoudre un système linéaire.

# Liens
https://www.cs.cmu.edu/~quake/triangle.html
https://github.com/luost26/laplacian-surface-editing/blob/master/main.py