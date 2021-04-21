from ..gobjects.spline import Drawing, Line
from ..io.svg import generate_svg_file
from ..utils.functions import rdp

import matplotlib.pyplot as plt

class Tracer:
    
    def __init__(self):
        
        self.drawing = None
        
    def run(self, dwg):
        
        print('* TRACER *')
        
        self.drawing = dwg
        #self.drawing.scale(1.0)
        
        print('   -> Creating B-Splines')
        
        for ln in self.drawing.lines:
            
            ln.pixels = rdp(ln.pixels, 1.5)
            
            ln.n_data_points = ln.pixels.shape[0]
            ln.n_control_points = ln.pixels.shape[0]
            
            try:
                ln.compute_params()
                ln.compute_knot_vector()
                ln.interpolate()
                print('ok')
                ln.bezier_subdivide()
            except:
                pass
            
            
            #try:
                #ln.prep()
                #ln.compute_params()
                #ln.compute_knot_vector()
                #ln.approximate()
                #ln.check_deviation()
                #ln.bezier_subdivide()
            #except:
                #pass
            
        print('   -> Converting to SVG')
        
        generate_svg_file(self.drawing)
        
    def run2(self, dwg):
        
        print('* TRACER *')
        
        self.drawing = dwg
        
        print('   -> Creating B-Splines')
        
        for step in [20, 18, 16, 14, 12, 10, 8]:
        
            for ln in self.drawing.lines:

                if not ln.valid:

                    try:
                        ln.prep(step)
                        ln.compute_params()
                        ln.compute_knot_vector()
                        ln.approximate()
                        ln.check_deviation(5.0)
                        
                    except:
                        pass

                    if ln.valid:
                    
                        try:
                            ln.reduce_thickness()
                            ln.bezier_subdivide()
                            ln.strokify()
                        except:
                            ln.valid = False
                            pass
            
        print('   -> Converting to SVG')
        
        generate_svg_file(self.drawing)
        
        
        
        
            
        