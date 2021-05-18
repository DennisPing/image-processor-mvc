import numpy as np
from time import time
from model.filters.boxed import Boxed 


class Pixelate(Boxed):

	def __init__(self):
		pass

	def apply(self, matrix, numSuperPixels):
		return self.naive_pixelate(matrix, numSuperPixels)

	def naive_pixelate(self, matrix, numSuperPixels):
		width = matrix.shape[0]
		height = matrix.shape[1]
		mod_matrix = np.zeros((width, height, 3))

		self.calc_offsets(matrix, numSuperPixels)

		# Fill in the perfect squares
		kernel = np.array((self.squareSize, self.squareSize))
		subsection = matrix[0:self.widthBoundary, 0:self.heightBoundary, :]
		self._replace_colors(matrix, mod_matrix, width - self.widthBoundary, height - self.heightBoundary, kernel)
		
		row_idx = np.arange(0, subsection.shape[0])
		col_idx = np.arange(0, subsection.shape[1])
		row_idx, col_idx = np.meshgrid(row_idx, col_idx, indexing="ij")

		kernel_row_idx = np.arange()

		
		return mod_matrix

	def _replace_colors(self, matrix, mod_matrix, row_bound, col_bound, kernel):
		kernelW = kernel.shape[0]
		kernelH = kernel.shape[1]
		kernelArea = kernelW * kernelH

		

