import csv
from pprint import pprint
import numpy as np
from numba import njit, types, typed
from time import time
import sys
from model.filters.boxed import Boxed

# @njit
# def _redmean(r1, g1, b1, r2, g2, b2):
#     redAvg = types.double((r1 + r2) / 2)
#     return types.double((2 + redAvg / 2) * (r2 - r1)**2 + (4 * (g2 - g1)**2) + (2+ (255 - redAvg) / 256) * (b2 - b1)**2)

# @njit
# def replaceColor(matrix, palette):
#     dmc = typed.List()
#     for x in palette:
#         dmc.append(typed.List(x))
#     # for x in palette:
#     #     dmc.append(x)
#     width = matrix.shape[0]
#     height = matrix.shape[1]
#     mod_matrix = np.zeros((width, height, 3))
#     for row in range(width):
#         for col in range(height):
#             r1 = matrix[row, col, 0]
#             g1 = matrix[row, col, 1]
#             b1 = matrix[row, col, 2]

#             closestDist = sys.maxsize

#             for each in dmc:
#                 dist = _redmean(r1, g1, b1, types.int64(each[1]), types.int64(each[2]), types.int64(each[3]))
#                 if dist < closestDist:
#                     closestDist = dist
#                     #closestDmc = each

#                     r = types.int64(each[1])
#                     g = types.int64(each[2])
#                     b = types.int64(each[3])
#             mod_matrix[row, col, 0] = r
#             mod_matrix[row, col, 1] = g
#             mod_matrix[row, col, 2] = b
#     return mod_matrix

class Dmc(Boxed):
    def __init__(self):
        pass

    def apply(self, matrix, numSuperPixels):

        with open('/Users/dennisping/Documents/image-processor-mvc/res/dmc-colors.csv', encoding='utf-8', newline='') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            palette = list(csv_reader)
        t0 = time()
        mod_matrix = self.naive_pixelate(matrix, numSuperPixels, palette)
        print(time() - t0)
        return mod_matrix
        
    def naive_pixelate(self, matrix, numSuperPixels, palette):
        """
        Pixelate an image based on the number of superpixels you want across an image (horizontal).
        Each superpixel's size is different in length or width by no more than 1 pixel, thus making
        all superpixels as close to square as possible.
        This implementation splits the image into 4 sectors and pixelates.
        """
        if numSuperPixels <= 0:
            raise ValueError("Number of superpixels cannot be 0 or negative")
        if numSuperPixels > matrix.shape[1] or numSuperPixels > matrix.shape[0]:
            raise ValueError(f"Number of superpixels cannot be greater than '{min(matrix.shape[1], matrix.shape[0])}'")
        
        width = matrix.shape[0]
        height = matrix.shape[1]

        self.calc_offsets(matrix, numSuperPixels)

        # Fill in the perfect squares
        for row in range(0, width - self.widthBoundary, self.squareSize):
            for col in range(0, height - self.heightBoundary, self.squareSize):
                matrix[row:row+self.squareSize, col:col+self.squareSize] = \
                self._replace_colors_dmc(matrix, row, col, self.squareSize, self.squareSize, palette)
        
        if self.offsetRows:
            # Fill in the bottom row offset
            for row in range(width - self.widthBoundary, width, self.offsetRowsWidth):
                for col in range(0, height - self.heightBoundary, self.squareSize):
                    matrix[row:row+self.offsetRowsWidth, col:col+self.squareSize] = \
                    self._replace_colors_dmc(matrix, row, col, self.offsetRowsWidth, self.squareSize, palette)

        if self.offsetCols:
            # Fill in the right column offset
            for row in range(0, width - self.widthBoundary, self.squareSize):
                for col in range(height - self.heightBoundary, height, self.offsetColsHeight):
                    matrix[row:row+self.squareSize, col:col+self.offsetColsHeight] = \
                    self._replace_colors_dmc(matrix, row, col, self.squareSize, self.offsetColsHeight, palette)
        
        if self.offsetRows and self.offsetCols:
            # Fill in the bottom right corner offset
            for row in range(width - self.widthBoundary, width, self.offsetRowsWidth):
                for col in range(height - self.heightBoundary, height, self.offsetColsHeight):
                    matrix[row:row+self.offsetRowsWidth, col:col+self.offsetColsHeight] = \
                    self._replace_colors_dmc(matrix, row, col, self.offsetRowsWidth, self.offsetColsHeight, palette)
        return matrix
		
    def _replace_colors_dmc(self, matrix, row, col, sqVert, sqHoriz, palette):
        avg = matrix[row:row+sqVert, col:col+sqHoriz].mean(axis=(0,1))
        closestDist = sys.maxsize
        for each in palette:
            r2 = int(each[1])
            g2 = int(each[2])
            b2 = int(each[3])
            dist = self._redmean(avg[0], avg[1], avg[2], r2, g2, b2)
            if dist < closestDist:
                closestDist = dist
                r = r2
                g = g2
                b = b2
        return [r, g, b]

    def _redmean(self, r1, g1, b1, r2, g2, b2):
        redAvg = (r1 + r2) / 2
        return (2 + redAvg / 2) * (r2 - r1)**2 + (4 * (g2 - g1)**2) + (2+ (255 - redAvg) / 256) * (b2 - b1)**2
        
