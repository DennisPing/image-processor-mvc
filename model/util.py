import os
import numpy as np
import logging
from PIL import Image

def readImage(filename):
    """ 
    Read an image file into a 3d numpy array. It can read both RGB and RGBA images.
    """
    if filename is None:
        raise TypeError("Filename is None")
    try:
        img = Image.open(filename)
        matrix = np.asarray(img)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            matrix = rgba2rgb(matrix)
        return matrix.astype(int)
    except FileNotFoundError as e:
        raise e

def writeImage(matrix, filename):
    """ 
    Write a 3d numpy array to an image file. Default output format is PNG.
     """
    if matrix is None:
        raise TypeError("Matrix is None")
    if filename is None:
        raise TypeError("Filename is None")
    # if extension is None:
    #     raise TypeError("Extension is None")
    try:
        # FUTURE: SAVE AS PNG BY DEFAULT
        image = Image.fromarray(np.uint8(matrix)).convert('RGB')
        image.save(filename)
    except OSError:
        raise OSError("Unable to write image file")

def getWidth(matrix):
    """ 
    The width is vertical side of the image. Because you iterate through the rows first. 
    """
    return len(matrix)

def getHeight(matrix):
    """ 
    The height is the horizontal side of the image. Because you iterate through the columns second. 
    """
    return len(matrix[0])

def getImage(matrix):
    """ 
    Convert the 3d numpy array back into an image. 
    """
    return Image.fromarray(np.uint8(matrix)).convert('RGB')

def rgba2rgb( rgba, background=(255,255,255) ):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B

    return np.asarray( rgb, dtype='uint8' )