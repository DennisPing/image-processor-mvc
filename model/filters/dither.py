import numpy as np
from time import time
from numba import njit

@njit
def _findClosestPaletteColor(oldPixel):
    palette = np.array([0, 36, 72, 108, 144, 180, 216, 252])
    temp = np.abs(palette - oldPixel)
    idxNew = temp.argmin()
    return palette[idxNew]

@njit
def applyError(matrix):
    width = matrix.shape[0]
    height = matrix.shape[1]
    depth = matrix.shape[2]
    for row in range(width):
            for col in range(height):
                for ch in range(depth): 
                    oldPixel = matrix[row, col, ch]
                    newPixel = _findClosestPaletteColor(oldPixel)
                    error = oldPixel - newPixel
                    matrix[row, col, ch] = newPixel

                    # diffuse right
                    if col + 1 < height:
                        value1 = matrix[row, col + 1, ch] + (error * 7/16)
                        value1 = int(value1)
                        value1 = max(min(255, value1), 0)
                        matrix[row, col + 1, ch] = value1

                    # diffuse left and down
                    if col - 1 > 0 and row + 1 < width:
                        value2 = matrix[row + 1, col - 1, ch] + (error * 3/16)
                        value2 = int(value2)
                        value1 = max(min(255, value2), 0)
                        matrix[row + 1, col - 1, ch] = value2

                    # diffuse down
                    if row + 1 < width:
                        value3 = matrix[row + 1, col, ch] + (error * 5/16)
                        value3 = int(value3)
                        value1 = max(min(255, value3), 0)
                        matrix[row + 1, col, ch] = value3

                    # diffuse right and down
                    if col + 1 < height and row + 1 < width:
                        value4 = matrix[row + 1, col + 1, ch] + (error * 1/16)
                        value4 = int(value4)
                        value1 = max(min(255, value4), 0)
                        matrix[row + 1, col + 1, ch] = value4
    return matrix
    

class Dither:

    def __init__(self):
        pass

    def apply(self, matrix):
        t1 = time()
        mod_matrix = applyError(matrix)
        print(time() - t1)
        return mod_matrix

    # def _calcError(self, matrix, row_idx, col_idx):
    #         oldPixel = matrix[row_idx, col_idx]
    #         newPixel = self._findClosestPaletteColor(oldPixel)
    #         error = oldPixel - newPixel
    #         return error

    # def _diffuse(self, matrix, row, col, ch, error, coefficient):
    # 	value = np.add(matrix[row, col, ch], np.multiply(error, coefficient))
    # 	value = np.clip(value.astype(int), 0, 255)
    # 	return value
