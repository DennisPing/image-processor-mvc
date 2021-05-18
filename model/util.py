import os
import numpy as np
import logging
from PIL import Image

""" Read an image file into a 3d numpy array. """
def readImage(filename):
    if filename is None:
        raise TypeError("Filename is None")
    try:
        matrix = np.asarray(Image.open(filename))
        return matrix.astype(int)
    except FileNotFoundError as e:
        raise e

""" Write a 3d numpy array to an image file. """
def writeImage(matrix, filename):
    if matrix is None:
        raise TypeError("Matrix is None")
    if filename is None:
        raise TypeError("Filename is None")
    # if extension is None:
    #     raise TypeError("Extension is None")
    try:
        image = Image.fromarray(np.uint8(matrix)).convert('RGB')
        image.save(filename)
    except OSError:
        raise OSError("Unable to write image file")

""" The width is vertical side of the image. Because you iterate through the rows first. """
def getWidth(matrix):
    return len(matrix)

""" The height is the horizontal side of the image. Because you iterate through the columns second. """
def getHeight(matrix):
    return len(matrix[0])

""" Convert the 3d numpy array back into an image. """
def getImage(matrix):
    return Image.fromarray(np.uint8(matrix)).convert('RGB')

""" Make a copy of the matrix to avoid accidental overwrites """
def makeCopy(matrix):
    width = matrix.shape[0]
    height = matrix.shape[1]
    depth = matrix.shape[2]
    copy = np.zeros((width, height, depth))
    for row in range(width):
        for col in range(height):
            for channel in range(depth):
                copy[row][col][channel] = matrix[row][col][channel]
    return copy
