import numpy as np

import matplotlib.pyplot as plt

from skimage import io


# RAVEL --------------------------------------------------------------------------------------

def display_ravel_vector(ravel):
    
    # Trace the edges
    
    for edg in ravel.edges:
    
        xx, yy = zip(*edg.pixels)
        plt.plot(yy, xx)
        
    # Spot the vertices
    
    for vx in ravel.vertices:
    
        x, y = vx.coord
        plt.scatter(y,x)
    
    plt.axis('equal')
    plt.gca().invert_yaxis()
    
    plt.show()
    
def display_ravel_raster(ravel):
    
    rst = np.zeros(ravel.distance_map.shape, dtype=bool)
    
    for edg in ravel.edges:
        for px in edg.pixels:
            rst[tuple(px.astype(int))] = True
    
    io.imshow(ravel.distance_map*(~rst))
    io.show()
    
# DRAWING ------------------------------------------------------------------------------------

def display_line(line):
    
    xx, yy = zip(*line.pixels)
    plt.plot(yy, xx)
    
    plt.axis('equal')
    plt.gca().invert_yaxis()
    
    plt.show()
