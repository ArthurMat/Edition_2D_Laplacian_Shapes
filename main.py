#!/usr/bin/env python3

import sys
from file_reader import to_dict
from interface import *




def main():
    points, seg = to_dict(sys.argv[1])
    main_interface(points, seg)


if __name__ == '__main__':
    main()
