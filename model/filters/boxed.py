from abc import ABCMeta
import numpy as np
import math

class Boxed(metaclass = ABCMeta):

    def __init__(self):
        self.squareSize = 0
        self.offsetRows = 0
        self.offsetRowsWidth = 0
        self.offsetCols = 0
        self.offsetColsHeight = 0
        self.widthBoundary = 0
        self.heightBoundary = 0
        self.normalRows = 0
        self.normalCols = 0

    def calc_offsets(self, matrix, numSuperPixels):
        width = matrix.shape[0]
        height = matrix.shape[1]

    #     self.squareSize = math.floor(height / numSuperPixels)
    #     A = np.array([[self.squareSize, self.squareSize + 1], [1, 1]])
    #     B = np.array([[height, numSuperPixels]])
    #     z = np.linalg.solve(A, B)
    #     self.normalCols = z[0]
    #     self.offsetCols = z[1]

        # Calculate the widths (vertical)
        self.squareSize = math.floor(width / numSuperPixels)
        self.offsetRowsWidth = self.squareSize + 1
        self.offsetRows = width % numSuperPixels
        self.normalRows = numSuperPixels - self.offsetRows

        # Calculate the heights (horizontal)
        temp = math.floor(height / self.squareSize)
        self.offsetCols = height % self.squareSize
        self.normalCols = temp - self.offsetCols
        self.offsetColsHeight = self.squareSize + 1

        # print(f"squareSize = {self.squareSize}")
        # print()
        # print(f"normalRows = {self.normalRows}")
        # print(f"normalCols = {self.normalCols}")
        # print()
        # print(f"offsetRows = {self.offsetRows}")
        # print(f"offsetCols = {self.offsetCols}")

        # Check for incompatible user input
        if self.normalRows < 0 or self.normalCols < 0:
            raise ValueError(f"Sorry, the number of superpixels '{numSuperPixels}' \
                is incompatible  with the dimensions of this image '{width}x{height}'")

        # If there are no uneven rows, set the width boundary to 0
        if self.offsetRows == 0:
            self.widthBoundary = 0
        else: # Set an internal width boundary
            self.widthBoundary = self.offsetRowsWidth * self.offsetRows

        # If there are no uneven cols, set the height boundary to 0
        if self.offsetCols == 0:
            self.heightBoundary = 0
        else: # Set an internal height boundary
            self.heightBoundary = self.offsetColsHeight * self.offsetCols
