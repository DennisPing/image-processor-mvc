import numpy as np
from model.filters.convolute import Convolute

class Blur(Convolute):

	def __init__(self):
		pass

	def apply(self, matrix):
		kernel = np.array([[0.0625, 0.125, 0.0625], 
							[0.125, 0.250, 0.125], 
							[0.0625, 0.125, 0.0625]])
		return self.fast_convolution(matrix, kernel)
