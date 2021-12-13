#!/usr/bin/env python3

from triangulate import *
from file_reader import *
from tools import *
from copy import deepcopy

class Data:
    def __init__(self, filename):
        self.filename = filename
        self.WIDTH = 0
        self.HEIGHT = 0
        self.poly_points, self.poly_seg = to_dict(self.filename)
        triangulate(self.filename)  # mettre le '-a.01' en option pour choisir le maillage
        arr1, arr2 = get_datas(self.filename[:-5])
        self.mesh_points, self.mesh_seg = array_to_dict(arr1), array_to_dict(arr2)
        self.copy_poly = deepcopy(self.poly_points)
        self.copy_mesh = deepcopy(self.mesh_points)
        self.points, self.seg = dict(), dict()
        self.copy_points = deepcopy(self.points)
        self.liste_cercles = []
        self.save_poly = []
        self.save_mesh = []
        self.save_points = []
        self.load = False

    def transform(self):
        self.poly_points = to_pygame(self.poly_points, self.WIDTH, self.HEIGHT)
        self.mesh_points = to_pygame(self.mesh_points, self.WIDTH, self.HEIGHT)
    
    def redim(self):
        # self.points = redimension(self.points, self.WIDTH, self.HEIGHT)
        self.poly_points = redimension(self.poly_points, self.WIDTH, self.HEIGHT)
        self.mesh_points = redimension(self.mesh_points, self.WIDTH, self.HEIGHT)

    def switch(self):
        self.load = not self.load
        if self.load:
            self.save_mesh = deepcopy(self.save_points)
            self.mesh_points = deepcopy(self.points)
            self.points, self.seg = deepcopy(self.poly_points), deepcopy(self.poly_seg)
            self.save_points = deepcopy(self.save_poly)
        else:
            self.save_poly = deepcopy(self.save_points)
            self.poly_points = deepcopy(self.points)
            self.points, self.seg = deepcopy(self.mesh_points), deepcopy(self.mesh_seg)
            self.save_points = deepcopy(self.save_mesh)
        self.copy_points = deepcopy(self.points)
        self.reset()

    def reset(self):
        self.liste_cercles = []
        # self.save_points = []
    
    def save(self):
        self.copy_poly = deepcopy(self.poly_points)
        self.copy_mesh = deepcopy(self.mesh_points)