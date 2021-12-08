#!/usr/bin/env python3

import sys
from file_reader import to_dict
from interface import *




def main():
    print("\nTo switch from the SELECT mode to the MOVE mode, push on 'S' or click on the colored cirlces !\n")
    points, seg = to_dict(sys.argv[1])
    # print(points, end='\n\n')
    # print(seg)
    main_interface(points, seg)


if __name__ == '__main__':
    main()
