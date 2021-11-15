#!/usr/bin/env python3

"""
Programme : pyhack
Créateur : Arthur Mathais
Date de création : 10/12/19
"""
##### Les imports :

from tkinter import *
from random import *
from math import sqrt

#############################
#                           #
#   Création des classes :  #
#                           #
#############################


####### Classe Niveau #######

class Niveau:
    """C'est ici qu'on va gérer les différents niveux"""

    def __init__(self, nb_de_piece):
        self.lvl = 1
        self.nb_de_piece = nb_de_piece
        self.pieces = []
        self.couloirs = []

    def augmenter_la_difficulte(self, tableau_de_jeu, tklist):
        self.lvl += 1
        self.nb_de_piece = (self.nb_de_piece * 2) // 1.5
        self.pieces = []
        self.couloirs = []
        tableau_de_jeu.mat = [[0 for _ in range(100)] for _ in range(100)]
        tklist[0].destroy()
        lancement_niveau(self)


    def ajouter_piece(self, liste_des_pieces, tklist, couleur="#9ACD32"):
        self.pieces.append(Piece(liste_des_pieces, tklist, couleur))

    def ajouter_couloir(self, coord_x, coord_y, liste_des_pieces, tklist,
                        couleur="#9ACD32"):
        self.couloirs.append(Couloir(coord_x, coord_y, liste_des_pieces,
                                     tklist, couleur))


####### Classe Tableau #######

class Tableau:
    """On reparti l'affichage dans un tableau de 100*100
        avec 1 case --> 8*8 pixel."""

    def __init__(self, largeur, hauteur):
        self.mat = [[0 for _ in range(largeur)] for _ in range(hauteur)]

    def __str__(self):
        """Permet de print() la classe Tableau
           (de manière lisible sur mon ordinateur)"""

        txt = "["
        for ligne in self.mat:
            txt += "["
            for i in ligne:
                txt += "{},".format(i)
            txt = txt[:-1]
            txt += "]\n"
        txt = txt[:-1]
        txt += "]"
        return txt

    def ajout_salles(self, salle):
        for x in range(salle.x[0] // 8, (1 + salle.x[1]) // 8):
            for y in range(salle.y[0] // 8, (1 + salle.y[1]) // 8):
                self.mat[y][x] = 1

    def ajout_couloirs(self, coul):
        mini_x = min(coul.coord_x[0] // 8, (1 + coul.coord_x[1]) // 8)
        maxi_x = max(coul.coord_x[0] // 8, (1 + coul.coord_x[1]) // 8)
        for x in range(mini_x, maxi_x):
            mini_y = min(coul.coord_y[0] // 8, (1 + coul.coord_y[1]) // 8)
            maxi_y = max(coul.coord_y[0] // 8, (1 + coul.coord_y[1]) // 8)
            for y in range(mini_y, maxi_y):
                self.mat[y][x] = 1

    def personnage(self, anciennes_coord, joueur):
        x = joueur.coordonnees[0]
        y = joueur.coordonnees[1]
        self.mat[y // 8][x // 8] = 2
        self.mat[anciennes_coord[1] // 8][anciennes_coord[0] // 8] = 1


####### Classe Piece #######

class Piece:
    """classe définissant la hauteur et la largeur des pieces"""

    def __init__(self, liste_des_pieces, tklist, couleur="#9ACD32"):
        self.couleur = couleur
        colision = True
        cpt_boucle = 0
        while colision:
            cpt_boucle += 1
            nbr_colision = 0
            xmin = 8 * randint(1, 84)
            ymin = 8 * randint(1, 84)
            xmax = xmin + 8 * randint(10, 15)
            ymax = ymin + 8 * randint(10, 15)
            for piece in liste_des_pieces.pieces:
                if (((piece.x[0] - 16) <= xmin <= (piece.x[1] + 16) or
                   (piece.x[0] - 16) <= xmax <= (piece.x[1] + 16)) and
                    ((piece.y[0] - 16) <= ymin <= (piece.y[1] + 16) or
                     (piece.y[0] - 16) <= ymax <= (piece.y[1] + 16))):
                    nbr_colision += 1
                    break
            if nbr_colision == 0:
                colision = False
            elif cpt_boucle > 50000:
                colision = False
        if cpt_boucle < 50000:
            self.x = [xmin, xmax]
            self.y = [ymin, ymax]

    def affiche(self, tklist):
        """méthode permettant d'afficher les pièces"""

        tklist[1].create_rectangle(self.x[0], self.y[0], self.x[1], self.y[1],
                                   fill=self.couleur, outline=self.couleur)


####### Classe Couloir #######

class Couloir:
    """Cette classe va permettre de relier les salles par des couloirs."""

    def __init__(self, coord_x, coord_y, liste_des_pieces, tklist,
                 couleur="#9ACD32"):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.couleur = couleur

    def affiche(self, tklist):
        """méthode permettant d'afficher les couloirs"""

        tklist[1].create_rectangle(self.coord_x[0], self.coord_y[0],
                                   self.coord_x[1], self.coord_y[1],
                                   fill=self.couleur, outline=self.couleur)


####### Classe joueur #######

class Joueur():
    """Classe pour definir le Joueur, ces mouvements..."""

    def __init__(self, liste_des_pieces, tklist, tableau_de_jeu,
                 couleur="red"):
        self.couleur = couleur
        self.coordonnees = []
        self.alea = None

    def placer_joueur(self, liste_des_pieces, tklist):
        self.alea = randint(0, len(liste_des_pieces.pieces) - 1)
        x = liste_des_pieces.pieces[self.alea].x
        y = liste_des_pieces.pieces[self.alea].y
        self.coordonnees = millieu(x, y)

    def mouvements(self, nbr_x, nbr_y, liste_des_pieces, tklist,
                   tableau_de_jeu):
        if tableau_de_jeu.mat[(self.coordonnees[1] + nbr_y) // 8][
                (self.coordonnees[0] + nbr_x) // 8] == 3:
            print("Félicitation vous passez au niveau suivant.")
            liste_des_pieces.augmenter_la_difficulte(tableau_de_jeu, tklist)
        elif tableau_de_jeu.mat[(self.coordonnees[1] + nbr_y) // 8][
                (self.coordonnees[0] + nbr_x) // 8] != 0:
            x0 = self.coordonnees[0]
            y0 = self.coordonnees[1]
            x1 = self.coordonnees[0] + 8
            y1 = self.coordonnees[1] + 8
            tklist[1].create_rectangle(x0, y0, x1, y1,
                                       fill="#9ACD32", outline="#9ACD32")
            self.coordonnees[0] += nbr_x
            self.coordonnees[1] += nbr_y
            self.actualise([x0, y0], liste_des_pieces, tklist, tableau_de_jeu)

    def actualise(self, anciennes_coord, liste_des_pieces, tklist,
                  tableau_de_jeu, couleur="red"):
        x0 = self.coordonnees[0]
        y0 = self.coordonnees[1]
        x1 = self.coordonnees[0] + 8
        y1 = self.coordonnees[1] + 8
        tklist[1].create_rectangle(x0, y0, x1, y1, fill=self.couleur)
        if anciennes_coord is not None:
            tableau_de_jeu.personnage(anciennes_coord, self)
        # print(tableau_de_jeu)


####### Classe Sortie #######

class Sortie():
    """Classe qui va définir la sortie du labirynthe
       et lancer le niveau suivant"""

    def __init__(self, liste_des_pieces, tklist, tableau_de_jeu, joueur,
                 couleur="blue"):
        self.couleur = couleur
        self.coordonnees = []

    def placer_sortie(self, liste_des_pieces, tklist, tableau_de_jeu, joueur):
        u = 1
        while u == joueur.alea:
            u = randint(0, len(liste_des_pieces.pieces) - 1)
        x = liste_des_pieces.pieces[u].x
        y = liste_des_pieces.pieces[u].y
        self.coordonnees = millieu(x, y)
        yy = self.coordonnees[1]
        xx = self.coordonnees[0]
        tableau_de_jeu.mat[yy // 8][xx // 8] = 3
        tklist[1].create_rectangle(xx, yy, xx + 8, yy + 8, fill=self.couleur)


###############################
#                             #
#   Création des fonctions :  #
#                             #
###############################

def millieu(x, y):
    return [((x[1] // 8 + x[0] // 8) // 2) * 8,
            ((y[1] // 8 + y[0] // 8) // 2) * 8]


def millieu8(x, y):
    return [((x[1] // 8 + x[0] // 8) // 2), ((y[1] // 8 + y[0] // 8) // 2)]


def distance(piece1, piece2):
    # je boucle pour regarder un par un qui est le plus proche
    # j'en fait une liste avec [a, b] == [b, a] donc pas de double
    mil_piece1 = millieu(piece1.x, piece1.y)
    mil_piece2 = millieu(piece2.x, piece2.y)
    dist = sqrt((mil_piece1[0] - mil_piece2[0])**2 +
                (mil_piece1[1] - mil_piece2[1])**2)
    return dist


def createur_couloir(liste_des_pieces, tklist):
    liste_salle_deja_reliee = []
    liste_couple = []
    dist_max = 0
    couple_loin = []
    dist_min = 100000
    couple = None
    cmpt1 = 0
    cmpt2 = 0
    for salle1 in liste_des_pieces.pieces:
        cmpt1 += 1
        for salle2 in liste_des_pieces.pieces:
            cmpt2 += 1
            if cmpt1 != cmpt2:
                if (salle2, salle1) not in liste_salle_deja_reliee:
                    if (salle1, salle2) not in liste_salle_deja_reliee:
                        dist = distance(salle1, salle2)
                        if dist < dist_min:
                            dist_min = dist
                            couple = [millieu8(salle1.x, salle1.y),
                                      millieu8(salle2.x, salle2.y)]
                            liste_salle_deja_reliee.append((salle1, salle2))
                        if dist > dist_max:
                            dist_max = dist
                            couple_loin = [millieu8(salle1.x, salle1.y),
                                           millieu8(salle2.x, salle2.y)]
        if couple not in liste_couple:
            liste_couple.append(couple)
        dist_min = 100000
        cmpt2 = 0
    liste_couple.append(couple_loin)
    return liste_couple


def remplir_trou_droit(tableau_de_jeu, tklist):
    liste_coins = []
    for y in range(1, len(tableau_de_jeu.mat)):
        for x in range(1, len(tableau_de_jeu.mat[y])):
            if (tableau_de_jeu.mat[y][x] == 1 and
                tableau_de_jeu.mat[y - 1][x] == 0 and
                tableau_de_jeu.mat[y + 1][x] == 0 and
                tableau_de_jeu.mat[y][x - 1] == 0 and
                (tableau_de_jeu.mat[y - 1][x - 1] == 1 or
                 tableau_de_jeu.mat[y + 1][x - 1] == 1)):

                liste_coins.append([x - 1, y])

    for i in liste_coins:
        tableau_de_jeu.mat[i[1]][i[0]] = 1
        tklist[1].create_rectangle(i[0] * 8, i[1] * 8,
                                   (i[0] + 1) * 8, (i[1] + 1) * 8,
                                   fill="#9ACD32", outline="#9ACD32")


def remplir_trou_gauche(tableau_de_jeu, tklist):
    liste_coins = []
    for y in range(1, len(tableau_de_jeu.mat)):
        for x in range(1, len(tableau_de_jeu.mat[y])):
            if (tableau_de_jeu.mat[y][x] == 1 and
                tableau_de_jeu.mat[y - 1][x] == 0 and
                tableau_de_jeu.mat[y + 1][x] == 0 and
                tableau_de_jeu.mat[y][x + 1] == 0 and
                (tableau_de_jeu.mat[y - 1][x + 1] == 1 or
                 tableau_de_jeu.mat[y + 1][x + 1] == 1)):

                liste_coins.append([x + 1, y])

    for i in liste_coins:
        tableau_de_jeu.mat[i[1]][i[0]] = 1
        tklist[1].create_rectangle(i[0] * 8, i[1] * 8,
                                   (i[0] + 1) * 8, (i[1] + 1) * 8,
                                   fill="#9ACD32", outline="#9ACD32")


def lancement_niveau(liste_des_pieces):
    tableau_de_jeu = Tableau(100, 100)

    fenetre = Tk()
    fenetre.title("Pyhack - Niveau {}".format(liste_des_pieces.lvl))
    can = Canvas(fenetre, width=800, height=800, bg='black')
    can.pack()

    tklist = [fenetre, can]

    joueur = Joueur(liste_des_pieces, tklist, tableau_de_jeu)

    for i in range(int(liste_des_pieces.nb_de_piece)):
        liste_des_pieces.ajouter_piece(liste_des_pieces, tklist)

    couloir_a_creer = createur_couloir(liste_des_pieces, tklist)
    i = 0

    for cloir in couloir_a_creer:
        i += 1
        x_dep = cloir[0][0] * 8
        x_arr = cloir[1][0] * 8
        y_dep = cloir[0][1] * 8
        y_arr = cloir[1][1] * 8
        liste_des_pieces.ajouter_couloir([x_dep, x_arr], [y_dep, y_dep + 8],
                                         liste_des_pieces, tklist)
        liste_des_pieces.ajouter_couloir([x_arr, x_arr + 8], [y_dep, y_arr],
                                         liste_des_pieces, tklist)

    for coul in liste_des_pieces.couloirs:
        coul.affiche(tklist)
        tableau_de_jeu.ajout_couloirs(coul)

    for nom in liste_des_pieces.pieces:
        nom.affiche(tklist)
        tableau_de_jeu.ajout_salles(nom)

    remplir_trou_gauche(tableau_de_jeu, tklist)

    joueur.placer_joueur(liste_des_pieces, tklist)


    joueur.actualise(None, liste_des_pieces, tklist, tableau_de_jeu)
    objectif = Sortie(liste_des_pieces, tklist, tableau_de_jeu, joueur)
    objectif.placer_sortie(liste_des_pieces, tklist, tableau_de_jeu, joueur)

    tklist[1].bind_all(
        "<KeyPress-s>", lambda event:
        joueur.mouvements(0, 8, liste_des_pieces, tklist, tableau_de_jeu))
    tklist[1].bind_all(
        "<KeyPress-z>", lambda event:
        joueur.mouvements(0, -8, liste_des_pieces, tklist, tableau_de_jeu))
    tklist[1].bind_all(
        '<KeyPress-d>', lambda event:
        joueur.mouvements(8, 0, liste_des_pieces, tklist, tableau_de_jeu))
    tklist[1].bind_all(
        '<KeyPress-q>', lambda event:
        joueur.mouvements(-8, 0, liste_des_pieces, tklist, tableau_de_jeu))
    tklist[0].mainloop()


#############################
#                           #
#   Reste du code :         #
#                           #
#############################


def main(nb_de_piece):
    liste_des_pieces = Niveau(nb_de_piece)
    lancement_niveau(liste_des_pieces)


if __name__ == '__main__':
    print("\nBienvenue dans le jeu Pyhack créé par Arthur Mathais.\n"
          "L'objectif est simple, vous incarnez un carré rouge "
          "et vous devez vous rendre au carré bleu.\n \n"
          "CONTROLES : \n  z --> aller en haut \n  s --> aller en bas \n"
          "  q --> aller en gauche \n  d --> aller en droite \n")
    main(3)
