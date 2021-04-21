import numpy as np

from skimage import img_as_float
from skimage.color import rgb2grey
from skimage.morphology import remove_small_holes, remove_small_objects, disk, skeletonize
from skimage.filters import threshold_sauvola, threshold_local, gaussian
from skimage.util import invert

from scipy.sparse import dok_matrix
from scipy.signal import convolve2d
from scipy.ndimage.morphology import distance_transform_edt

from ..utils.functions import laplacian_of_gaussian

class Preprocessor:
    
    DEFAULT_CONFIG = {
        "pen_diameter": 20,
        "window_size": 99,
        "dot_threshold": 1300,
    }
    
    def __init__(self, cfg = DEFAULT_CONFIG):
        
        self.config = cfg
        
        self.input = None
        self.binary_layer = None
        self.distance_map = None
        self.ridges_layer = None
        self.skeleton_layer = None
        
        
    def convert_input(self):
        
        # Convert the input into a greyscale Numpy array
        
        self.input = img_as_float(rgb2grey(self.input))
        self.input = gaussian(self.input, sigma = 4)
        
    def binarize(self):
        
        # Perform an adaptive thresholding and filter out the artifacts
        # Return a binary as a boolean Numpy array
        
        thresh_sauvola = threshold_sauvola(self.input, self.config["window_size"])

        bin_image = self.input > thresh_sauvola
    
        # Filter out the small artifacts

        bin_image = remove_small_holes(bin_image)
        bin_image = remove_small_objects(bin_image)
        
        self.binary_layer = ~bin_image
        
    def make_distance_map(self):
        
        self.distance_map = distance_transform_edt(self.binary_layer)
        
    def extract_ridges(self):
        
        # Create the LoG kernel :
        
        m = 9
        sigma = 1.4
        
        kernel = np.zeros((m,m), np.float)
        
        #z = (x**2+y**2)/(2*sigma**2)
        #val = -(1-z)/(np.pi*sigma**4)*np.exp(-z)
        #return val
        
        for i in range(m):
            for j in range(m):
                kernel[i,j] = -(m**2)*laplacian_of_gaussian(i-m/2, j-m/2, sigma)
                
        # Perform the convolution
        
        ridges = convolve2d(self.distance_map, kernel, mode='same', boundary='fill', fillvalue=False)
        
        self.ridges_layer = skeletonize(ridges>40)
        
        
    def slideshow(self):
    
        return [self.input,
                self.binary_layer,
                self.distance_map,
                self.ridges_layer
               ]
        
    def run(self, inpt):
        
        print('* PREPROCESSOR *')
        self.input = inpt
        
        print('   -> Converting input')
        self.convert_input()
        
        print('   -> Binarization')
        self.binarize()
        
        print('   -> Euclidean distance transformation')
        self.make_distance_map()
        
        print('   -> Ridges extraction')
        self.extract_ridges()
        
        