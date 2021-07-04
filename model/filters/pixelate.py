import numpy as np
from time import time
from model.filters.boxed import Boxed

class Pixelate(Boxed):
    
    def __init__(self):
        pass

    def apply(self, matrix, numSuperPixels):
        return self.naive_pixelate(matrix, numSuperPixels)

    def naive_pixelate(self, matrix, numSuperPixels):
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

        t0 = time()
        width = matrix.shape[0]
        height = matrix.shape[1]

        self.calc_offsets(matrix, numSuperPixels)

        # Fill in the perfect squares
        for row in range(0, width - self.widthBoundary, self.squareSize):
            for col in range(0, height - self.heightBoundary, self.squareSize):
                matrix[row:row+self.squareSize, col:col+self.squareSize] = \
                self._replace_colors(matrix, row, col, self.squareSize, self.squareSize)
        
        if self.offsetRows:
            # Fill in the bottom row offset
            for row in range(width - self.widthBoundary, width, self.offsetRowsWidth):
                for col in range(0, height - self.heightBoundary, self.squareSize):
                    matrix[row:row+self.offsetRowsWidth, col:col+self.squareSize] = \
                    self._replace_colors(matrix, row, col, self.offsetRowsWidth, self.squareSize)

        if self.offsetCols:
            # Fill in the right column offset
            for row in range(0, width - self.widthBoundary, self.squareSize):
                for col in range(height - self.heightBoundary, height, self.offsetColsHeight):
                    matrix[row:row+self.squareSize, col:col+self.offsetColsHeight] = \
                    self._replace_colors(matrix, row, col, self.squareSize, self.offsetColsHeight)
        
        if self.offsetRows and self.offsetCols:
            # Fill in the bottom right corner offset
            for row in range(width - self.widthBoundary, width, self.offsetRowsWidth):
                for col in range(height - self.heightBoundary, height, self.offsetColsHeight):
                    matrix[row:row+self.offsetRowsWidth, col:col+self.offsetColsHeight] = \
                    self._replace_colors(matrix, row, col, self.offsetRowsWidth, self.offsetColsHeight)

        t1 = time()
        print(t1-t0)
        return matrix

    def _replace_colors(self, matrix, row, col, sqVert, sqHoriz):
        return matrix[row:row+sqVert, col:col+sqHoriz].mean(axis=(0,1))