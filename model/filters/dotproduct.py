from abc import ABCMeta, abstractmethod
import numpy as np
from time import time

class DotProduct(metaclass = ABCMeta):

	def naive_dotproduct(self, matrix, kernel):
		"""
		A naive approach which uses brute force loops. Very slow.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:param kernel: a 1d numpy array of size [length]
		:return: a convoluted 3d numpy array of size [width][height][channel]
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]
		mod_matrix = np.zeros((width, height, 3))

		for row in range(width):
			for col in range(height):
				r = matrix[row, col, 0]
				g = matrix[row, col, 1]
				b = matrix[row, col, 2]

				mod_matrix[row, col, 0] = r*kernel[0,0] + g*kernel[0,1] + b*kernel[0,2]
				mod_matrix[row, col, 1] = r*kernel[1,0] + g*kernel[1,1] + b*kernel[1,2]
				mod_matrix[row, col, 2] = r*kernel[2,0] + g*kernel[2,1] + b*kernel[2,2]
		t1 = time()
		print(t1-t0)
		mod_matrix = np.clip(mod_matrix.astype(int), 0, 255)
		return mod_matrix

	def fast_dotproduct(self, matrix, kernel):
		"""
		A fast dot product which uses Numpy's optimized dot product module.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:param kernel: a 1d numpy array of size [length]
		:return: a convoluted 3d numpy array of size [width][height][channel]
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]
		mod_matrix = np.zeros((width, height, 3))
		
		mod_matrix[:,:,0] = np.dot(matrix, kernel[0])
		mod_matrix[:,:,1] = np.dot(matrix, kernel[1])
		mod_matrix[:,:,2] = np.dot(matrix, kernel[2])
		
		mod_matrix = np.clip(mod_matrix.astype(int), 0, 255)
		t1 = time()
		print(t1-t0)
		return mod_matrix