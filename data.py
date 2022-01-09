#!/usr/bin/env python3

from triangulate import *
from file_reader import *
from tools import *
from copy import deepcopy
import os

class Data:
    def __init__(self, filename):
        self.filename = filename
        self.WIDTH = 0
        self.HEIGHT = 0
        if not os.path.exists(self.filename[:-5] + ".1.node"):
            triangulate(self.filename)  # mettre le '-a.01' en option pour choisir le maillage
        arr1, arr2 = get_datas(self.filename[:-5])
        self.points, self.seg = array_to_dict(arr1), array_to_dict(arr2)
        self.seg = dico_cleaner(self.seg)
        self.copy_points = deepcopy(self.points)
        self.handles = []
        self.fixes = []
        self.save_points = []
        self.day = 0
        self.indice_point = len(self.points.keys())
        self.indice_seg = len(self.seg.keys())

    def transform(self):
        self.points = to_pygame(self.points, self.WIDTH, self.HEIGHT)
    
    def redim(self):
        self.points = redimension(self.points, self.WIDTH, self.HEIGHT)

    def save(self):
        self.copy_points = deepcopy(self.points)

    def suppression(self):
        cles_s = []
        self.handles.sort(reverse = True)
        for k in self.handles:
            self.points.pop(k)
            for key, val in self.seg.items():
                if k in val and key not in cles_s:
                    cles_s.append(key)
        cles_s.sort(reverse = True)
        for k in cles_s:
            self.seg.pop(k)
        self.handles = []
    
    def suppr_seg(self, seg_proche):
        self.seg.pop(seg_proche)

    def update_keys(self):
        self.indice_point = len(self.points.keys()) + 1
        self.indice_seg = len(self.seg.keys()) + 1
        # k1 = range(1, self.indice_point)
        # k2 = range(1, self.indice_seg)
        # dic1 = dict((key, value) for (key, value) in zip(k1, self.points))
        # dic2 = dict((key, value) for (key, value) in zip(k2, self.seg))
        # self.points = deepcopy(dic1)
        # self.seg = deepcopy(dic2)
    
    def reset(self):
        arr1, arr2 = get_datas(self.filename[:-5])
        self.points, self.seg = array_to_dict(arr1), array_to_dict(arr2)
        self.seg = dico_cleaner(self.seg)
        self.copy_points = deepcopy(self.points)
        self.handles = []
        self.fixes = []
        self.save_points = []
        self.transform()
        self.redim()
        self.indice_point = len(self.points.keys())
        self.indice_seg = len(self.seg.keys())
