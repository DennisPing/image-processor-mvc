import numpy as np
from model.filters.convolute import Convolute

class Sharpen(Convolute):

	def __init__(self):
		pass
	
	def apply(self, matrix):
		kernel = np.array([[-0.125, -0.125, -0.125, -0.125, -0.125],
							[-0.125, 0.25, 0.25, 0.25, -0.125],
							[-0.125, 0.25, 1.00, 0.25, -0.125],
							[-0.125, 0.25, 0.25, 0.25, -0.125],
							[-0.125, -0.125, -0.125, -0.125, -0.125]])
		return self.fast_convolution(matrix, kernel)