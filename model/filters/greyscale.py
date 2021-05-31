import numpy as np
from model.filters.dotproduct import DotProduct

class Greyscale(DotProduct):

    def __init__(self):
        pass

    def apply(self, matrix):
        kernel = np.array([[0.2126, 0.7152, 0.0722],
                            [0.2126, 0.7152, 0.0722],
                            [0.2126, 0.7152, 0.0722]])
        return self.fast_dotproduct(matrix, kernel)