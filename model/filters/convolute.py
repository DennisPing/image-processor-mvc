from abc import ABCMeta, abstractmethod
from model import util
import numpy as np
from scipy.ndimage import convolve
from time import time

class Convolute(metaclass = ABCMeta):

	def naive_convolution(self, matrix, kernel):
		"""
		A naive convolution which uses brute force loops. Very slow.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:param kernel: a 2d numpy array of size [width][height]
		:return: a convoluted 3d numpy array of size [width][height][channel]
		"""
		self.width = matrix.shape[0]
		self.height = matrix.shape[1]

		mod_matrix = util.makeCopy(matrix)
		self.kernel_sum = self._kernelSum(kernel)

		offset = len(kernel) // 2

		for row in range(self.width):
			for col in range(self.height):
				for ch in range(3):
					
					accumulator = 0.0
					
					for j in range(len(kernel)):
						for k in range(len(kernel)):

							xcoord = row + j - offset
							ycoord = col + k - offset

							value = 0
							if xcoord < 0 or xcoord >= self.width or ycoord < 0 or ycoord >= self.height:
								value = matrix[row, col, ch]
							else:
								value = matrix[xcoord, ycoord, ch]
							accumulator += (value * kernel[j, k])
					
					average = self._clamp(accumulator) / self.kernel_sum
					mod_matrix[row, col, ch] = int(average)
		return mod_matrix

	def better_convolution(self, matrix, kernel):
		"""
		A better convolution which utilizes array braodcasting.
		About 2 times faster than the naive approach.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:param kernel: a 2d numpy array of size [width][height]
		:return: a convoluted 3d numpy array of size [width][height][channel]
		"""
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]
		kernel = np.flipud(np.fliplr(kernel))
		k = len(kernel)
		offset = k//2
		mod_matrix = np.zeros((width, height, 3))

		# extend the padding on all 4 sides, this is analogous to mode=nearest
		padded_matrix = np.zeros((width + offset*2, height + offset*2, 3))
		padded_matrix[offset:-offset, offset:-offset, :] = matrix
		for i in range(offset):
			padded_matrix[i,:,:] = padded_matrix[offset,:,:]
			padded_matrix[:,i,:] = padded_matrix[:,offset,:]
		for j in range(-1, -offset-1, -1):
			padded_matrix[j,:,:] = padded_matrix[-offset-1,:,:]
			padded_matrix[:,j,:] = padded_matrix[:,-offset-1,:]

		for row in range(width):
			for col in range(height):
				for ch in range(3):
					mod_matrix[row, col, ch] = (kernel * padded_matrix[row: row + k, col: col + k, ch]).sum()
		mod_matrix = np.clip(mod_matrix.astype(int), 0, 255)
		t1 = time()
		print(t1-t0)
		return mod_matrix

	def fast_convolution(self, matrix, kernel):
		t0 = time()
		width = matrix.shape[0]
		height = matrix.shape[1]
		kernel = np.flipud(np.fliplr(kernel))
		k = len(kernel)
		offset = k//2 # if kernel is 3x3 then offset is 1, if kernel is 5x5 then offset is 2
		mod_matrix = np.zeros((width, height, 3))

		# extend the padding on all 4 sides by 'offset' length
		padded_matrix = np.zeros((width + offset*2, height + offset*2, 3))
		padded_matrix[offset:-offset, offset:-offset] = matrix
		# add padding to north and west borders by copying edge pixel
		for i in range(offset):
			padded_matrix[i, :, :] = padded_matrix[offset, :, :]
			padded_matrix[:, i, :] = padded_matrix[:, offset, :]
		# add padding to east and south borders by copying edge pixel
		for j in range(-1, -offset-1, -1):
			padded_matrix[j, :, :] = padded_matrix[-offset-1, :, :]
			padded_matrix[:, j, :] = padded_matrix[:, -offset-1, :]

		# make a meshgrid for the matrix with coordinates (row_idx, col_idx)
		# coordinate (0,0) is at the top left corner of the matrix
		# row_idx and col_idx have the shape of (width, height)
		row_idx = np.arange(offset, padded_matrix.shape[0] - offset)
		col_idx = np.arange(offset, padded_matrix.shape[1] - offset)
		row_idx, col_idx = np.meshgrid(row_idx, col_idx, indexing="ij")

		# make a meshgrid for the kernel with coordinates (k_row_idx, k_col_idx)
		# coordinate (0,0) is at the center of the kernel
		# kernel_row_idx and kernel_col_idx have the shape of (k, k)
		kernel_row_idx = np.arange(kernel.shape[0]) - offset
		kernel_col_idx = np.arange(kernel.shape[1]) - offset
		kernel_row_idx, kernel_col_idx = np.meshgrid(kernel_row_idx, kernel_col_idx, indexing="ij")

		# insert 2 new dimensions at every position
		# adding the kernel indexes changes row_idx and col_idx to shape of (width, height, k, k)
		row_idx = row_idx[..., np.newaxis, np.newaxis] + kernel_row_idx
		col_idx = col_idx[..., np.newaxis, np.newaxis] + kernel_col_idx

		# do element wise multiply 
		# sum reduce the 2nd last and 3rd last dimensions
		mod_matrix = np.sum(padded_matrix[row_idx, col_idx] * kernel[..., np.newaxis], axis=(-2,-3))
		mod_matrix = np.clip(mod_matrix.astype(int), 0, 255)
		t1 = time()
		print(t1-t0)
		return mod_matrix

	def faster_convolution(self, matrix, kernel):
		"""
		A fast convolution which uses Scipy's optimized convolve module.
		:param matrix: a 3d numpy array of size [width][height][channel]
		:param kernel: a 2d numpy array of size [width][height]
		:return: a convoluted 3d numpy array of size [width][height][channel]
		"""
		width = matrix.shape[0]
		height = matrix.shape[1]
		mod_matrix = np.zeros((width, height, 3))
		padded_matrix = np.zeros((width + 2, height + 2, 3))
		padded_matrix[1:-1, 1:-1] = matrix

		for ch in range(3):
			channel = matrix[:,:,ch]
			mod_matrix[:,:,ch] = convolve(channel, kernel, mode='reflect')
	
		mod_matrix = np.clip(mod_matrix.astype(int), 0, 255)
		return mod_matrix
	
	def _kernelSum(self, kernel):
		sum = 0.0
		for i in range(kernel.shape[0]):
			for j in range(kernel.shape[1]):
				sum += kernel[i, j]
		return sum

	def _clamp(self, number):
		return max(0, min(255, int(number)))

