#!/usr/bin/env python3

import sys
import optparse
from file_reader import to_dict
from interface import *
from data import Data

def parametres():
    """
    définitions des options possibles
    """
    utilisation = "./%prog [options]"
    parser = optparse.OptionParser(usage=utilisation)
    parser.add_option("-W", "--width",
                      dest="WIDTH", default=750, type='int',
                      help="Vous permet de changer la largeur de la fenetre\n")
    parser.add_option("-H", "--height", 
                      dest="HEIGHT", default=750, type='int',
                      help="Vous permet de changer la heuteur de la fenetre\n")
    parser.add_option("-f", "-p", "--fichier", "--path",
                      dest="PATH", default="test/bicycle_seat.poly", type='str',
                      help="Vous permet de changer le chemin du fichier utilisé (les prefixes ne sont pas obligatoires, ne rien mettre devant le chemin marche aussi)\n")
    (option, args) = parser.parse_args()
    if option.WIDTH < 0:
        parser.error(f"\tAttention, vous avez rentré une valeur négative pour la largeur de la fenetre : {option.LIGNE}")
    if option.HEIGHT < 0:
        parser.error(f"\tAttention, vous avez rentré une valeur négative pour la hauteur de la fenetre : {option.COLONNE}")
    return option, args

def main():
    option, args = parametres()
    if len(sys.argv) == 1:
        data = Data(option.PATH)
    else:
        path = None
        for arg in sys.argv:
            if arg[:-5] == ".poly":
                path = arg
        if path is None:
            path = option.PATH
        data = Data(path)

    main_interface(data, option.WIDTH, option.HEIGHT)


if __name__ == '__main__':
    main()
