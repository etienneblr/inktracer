from ..gobjects.skeleton import Skeleton
from ..gobjects.pgraph import *

class PathFinder:
    
    def __init__(self, skel=None):
        
        self.skeleton = None
        self.ravel = None
        
    def pack(self):
        
        rvl = Ravel()
            
        # Create instances of vertex for each hub
            
        for hub in self.skeleton.hubs:
            vertex = Vertex()
            vertex.id = hub.tag
            vertex.coord = hub.pole
            
            rvl.vertices.append(vertex)
            
        # Create instances of edge for each path of the skeleton
        
        for path in self.skeleton.paths:
            edge = Edge()
            edge.id = path.tag
            edge.pixels = path.get_points()
            edge.start_vertex = rvl.vertices[path.start_vertex - 1] if path.start_vertex else None
            edge.end_vertex = rvl.vertices[path.end_vertex - 1] if path.end_vertex else None
            
            rvl.edges.append(edge)
            
        # Link everything up :
            
        for vertex in rvl.vertices:
            
            vertex.binding = [Socket(edg, True) for edg in rvl.edges if edg.start_vertex == vertex] + \
                            [Socket(edg, False) for edg in rvl.edges if edg.end_vertex == vertex]
            
        self.ravel = rvl
            
    
    def run(self, inpt):
        
        print('* PATHFINDER *')
        
        print('   -> Encoding skeleton')
        self.skeleton = Skeleton(inpt)
        
        print('   -> Separating hubs and paths')
        self.skeleton.split()
        
        print('   -> Extraction of Hub objects')
        self.skeleton.get_hubs()
        
        print('   -> Extraction of Path objects')
        self.skeleton.get_connected_paths()
        self.skeleton.get_standalone_paths()
        
        print('   -> Packing up')
        self.pack()
        
        self.skeleton = None