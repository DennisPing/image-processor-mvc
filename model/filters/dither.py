import numpy as np
from time import time

class Dither:

	flag = True

	def __init__(self):
		pass

	def apply(self, matrix):
		return self.naive_dither(matrix)

	def naive_dither(self, matrix):
		"""
		A naive dither which uses brute force loops. Very slow.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:return: a 3d numpy array which has Floyd Steinberg dithering applied to it
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]

		for row in range(width):
			for col in range(height):
				oldPixel = matrix[row, col]
				newPixel = self._findClosestPaletteColor(oldPixel)
				error = oldPixel - newPixel
				matrix[row, col] = newPixel

				# diffuse right
				if col + 1 < height:
					value1 = matrix[row, col + 1] + (error * 7/16)
					matrix[row, col + 1] = np.clip(value1.astype(int), 0, 255)

					# diffuse left and down
				if col - 1 > 0 and row + 1 < width:
					value2 = matrix[row + 1, col - 1] + (error * 3/16)
					matrix[row + 1, col - 1] = np.clip(value2.astype(int), 0, 255)

					# diffuse down
				if row + 1 < width:
					value3 = matrix[row + 1, col] + (error * 5/16)
					matrix[row + 1, col] = np.clip(value3.astype(int), 0, 255)

					# diffuse right and down
				if col + 1 < height and row + 1 < width:
					value4 = matrix[row + 1, col + 1] + (error/16)
					matrix[row + 1, col + 1] = np.clip(value4.astype(int), 0, 255)

		t1 = time()
		print(t1-t0)
		return matrix

	def test_dither(self, matrix):
		"""
		A better dither which utilizes array broadcasting.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:return: a 3d numpy array which has Floyd Steinberg dithering applied to it
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]
		
		row_idx = np.arange(0, width-1)
		col_idx = np.arange(1, height-1)
		row_idx, col_idx = np.meshgrid(row_idx, col_idx, indexing="ij")

		value1 = matrix[row_idx, col_idx + 1] + (self._calcError(matrix, row_idx, col_idx) * 7/16)
		matrix[row_idx, col_idx + 1] = np.clip(value1.astype(int), 0, 255)		
		t1 = time()
		print(t1-t0)
		return matrix


	def _calcError(self, matrix, row_idx, col_idx):
			oldPixel = matrix[row_idx, col_idx]
			newPixel = self._findClosestPaletteColor(oldPixel)
			error = oldPixel - newPixel
			return error
	
	def _findClosestPaletteColor(self, oldPixel):
		# if (colorBit != 2) and (colorBit != 4) and (colorBit != 8):
		# #if colorBit != 8:
		# 	raise ValueError("Invalid color bit.")
		# ceiling = 256 - (256 % (colorBit-1))
		# palette = np.linspace(0, ceiling, colorBit, dtype=int)
		# while self.flag == True:
		# 	print(palette)
		# 	self.flag = False
		palette = np.array([0, 36, 72, 108, 144, 180, 216, 252])
		
		idxR = (np.abs(palette - oldPixel[0])).argmin()
		idxG = (np.abs(palette - oldPixel[1])).argmin()
		idxB = (np.abs(palette - oldPixel[2])).argmin()
		return np.array([palette[idxR], palette[idxG], palette[idxB]])
	
	# def _diffuse(self, matrix, row, col, ch, error, coefficient):
	# 	value = np.add(matrix[row, col, ch], np.multiply(error, coefficient))
	# 	value = np.clip(value.astype(int), 0, 255)
	# 	return value
