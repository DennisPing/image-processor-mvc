import numpy as np
from random import randint
from time import time
from scipy.spatial.distance import cdist
from numba import njit, types, typed
import sys
import itertools

def applyMosaic(matrix, numSeeds):
    t1 = time()
    width = matrix.shape[0]
    height = matrix.shape[1]
    seeds = generateSeedsNumba(numSeeds, width, height)
    mod_matrix = fast_mosaic_Numba(matrix, seeds)
    print(time() - t1)
    return mod_matrix

@njit
def generateSeedsNumba(numSeeds, width, height):
    seedArray = set()
    while len(seedArray) < numSeeds:
        coord = (randint(0, width-1), randint(0, height-1))
        if coord not in seedArray:
            seedArray.add(coord)
    return typed.List(seedArray)

@njit
def findClosestPoint(row, col, seedArray):
    closestPoint = (sys.maxsize, sys.maxsize)
    closestDist = sys.maxsize
    for seed in seedArray:
        dist = ((row - seed[0]) ** 2) + ((col - seed[1]) ** 2)
        if dist < closestDist:
            closestDist = dist
            closestPoint = (seed[0], seed[1])
    return closestPoint

@njit
def fast_mosaic_Numba(matrix, seeds):
    """
    Use Numba to compile code.
    """
    width = matrix.shape[0]
    height = matrix.shape[1]
    mod_matrix = np.zeros((width, height, 3))

    for row in range(width):
        for col in range(height):
            closestPoint = findClosestPoint(row, col, seeds)
            r, c = closestPoint
            mod_matrix[row, col, 0] = matrix[r, c, 0]
            mod_matrix[row, col, 1] = matrix[r, c, 1]
            mod_matrix[row, col, 2] = matrix[r, c, 2]
    return mod_matrix


class Mosaic:

    def __init__(self):
        pass

    def apply(self, matrix, numSeeds):
        if matrix.shape[0] * matrix.shape[1] <= 408_960: # Under 480p
            return self.fast_mosaic(matrix, numSeeds)
        else:
            return applyMosaic(matrix, numSeeds)

    def better_mosaic(self, matrix, numSeeds):
        """
        Utilizes array broadcasting to find all possible seed distances for every element on the matrix.
        Very memory intensive because you need to compute [W x H x numSeeds] values.
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
        seedArray = set()
        while len(seedArray) < numSeeds:
            coord = (randint(0, width-1), randint(0, height-1))
            if coord not in seedArray:
                seedArray.add(coord)
        return np.array(list(seedArray))