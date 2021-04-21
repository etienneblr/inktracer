import numpy as np

from ..gobjects.pgraph import *
from ..gobjects.distmap import DistanceMap
from ..gobjects.spline import Drawing, Line
from ..io.display import display_ravel_vector, display_ravel_raster

class Optimizer:
    
    DEFAULT_CONFIG = {
        "pen_diameter": 20,
        "window_size": 99,
        "dot_threshold": 1300,
    }
    
    def __init__(self, cfg = DEFAULT_CONFIG):
        
        self.config = cfg
        self.ravel = None
        
    def pack(self):
        
        dwg = Drawing()
        
        for edg in self.ravel.edges:
            
            ln = Line()
            ln.pixels = edg.pixels
            ln.thickness = edg.thickness
            dwg.lines.append(ln)
            
        return dwg
        
    def run(self, rvl, d_map):
        
        print('* OPTIMIZER *')
        
        print('   -> Setting up distance map')
        
        self.ravel = rvl
        self.ravel.distance_map = DistanceMap(d_map)
        self.ravel.set_thickness()
        
        print('   -> Pruning')
        self.ravel.prune()
        
        print('   -> Clumping 3-vertices')
        self.ravel.process_3vertices()
        
        print('   -> Packing up')
        dwg = self.pack()
        
        return dwg

        
    