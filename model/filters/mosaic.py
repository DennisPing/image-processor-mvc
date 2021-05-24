import numpy as np
from random import randint
from time import time
from scipy.spatial.distance import cdist

class Mosaic:

	def __init__(self):
		pass

	def apply(self, matrix, numSeeds):
		return self.fast_mosaic(matrix, numSeeds)

	def better_mosaic(self, matrix, numSeeds):
		"""
		Utilizes array broadcasting to find all possible seed distances for every element on the matrix.
		Very memory intensive because you need to compute [W x H x numSeeds] values.
		Scales exponentially, thus a large enough seed may exeed RAM capacity.
		:param matrix: a 3d image numpy array of size [width][height][3]
		:param numSeeds: the number of random seeds to use on the image
		:return: a modified image with a mosaic effect
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]

		seeds = self._generateSeeds(numSeeds, width, height)

		# Make a meshgrid of my image matrix so that I have coordinates rather than RGB values from 0-255
		matrix_row_idx = np.arange(matrix.shape[0])
		matrix_col_idx = np.arange(matrix.shape[1])
		matrix_row, matrix_col = np.meshgrid(matrix_row_idx, matrix_col_idx, indexing="ij")

		# Split up my seeds into rows and columns. Shape is (S,) where S is numSeeds.
		seed_row = seeds[:, 0]
		seed_col = seeds[:, 1]

		# Ignore sqrt in calculation because we only care about relative distance.

		# Do matrix row coordinates - seed row coordinates. Shape is now W x H x S
		# Do matrix col coordinates - seed col coordinates. Shape is now W x H x S
		diff_row = matrix_row[..., np.newaxis] - seed_row
		diff_col = matrix_col[..., np.newaxis] - seed_col

		# For all elements, calculate the distance index. Then reduce to the minimum distance index.
		# Very memory heavy because I'm doing this for W x H x S elements!!!
		dist_idx = (diff_row ** 2) + (diff_col ** 2)
		min_dist_idx = dist_idx.argmin(axis=2)
		
		# Get the RGB seed colors from the image matrix. Shape is (S,3) where S is numSeeds.
		seed_colors = matrix[seed_row, seed_col, :]
		# Replace every 'dist_min_index' with its corresponding seed color.
		mod_matrix = seed_colors[min_dist_idx]
		t1 = time()
		print(t1-t0)
		return mod_matrix

	def fast_mosaic(self, matrix, numSeeds):
		"""
		A fast mosaic which uses Scipy's efficient cdist module.
		The performance is logarithmic so it scales better as numSeeds increases.
		:param matrix: a 3d image numpy array of size [width][height][3]
		:param numSeeds: the number of random seeds to use on the image
		:return: a modified image with a mosaic effect
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]

		seeds = self._generateSeeds(numSeeds, width, height)
		seed_colors = matrix[seeds[:, 0], seeds[:, 1], :]

		matrix_row_idx = np.arange(matrix.shape[0])
		matrix_col_idx = np.arange(matrix.shape[1])
		matrix_row, matrix_col = np.meshgrid(matrix_row_idx, matrix_col_idx, indexing="ij")

		matrix_coord = np.stack((matrix_row.ravel(), matrix_col.ravel()), axis=1)
		all_dist_idx = cdist(matrix_coord, seeds)
		
		min_dist_idx = all_dist_idx.argmin(axis=1)
		min_dist_idx = min_dist_idx.reshape((width, height))
		mod_matrix = seed_colors[min_dist_idx]
		
		t1 = time()
		print(t1-t0)
		return mod_matrix

	def _generateSeeds(self, numSeeds, width, height):
		cols = np.random.randint(height, size=numSeeds)
		rows = np.random.randint(width, size=numSeeds)
		seedArray = np.stack([rows, cols], axis=-1)
		return seedArray