#!/usr/bin/env python3

import sys
import pygame
from file_reader import to_dict




def main():
    points, seg = to_dict(sys.argv[1])
    print(points, end='\n\n')
    print(seg)


if __name__ == '__main__':
    main()
