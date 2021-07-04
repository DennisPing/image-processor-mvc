from model import util
from model.filters import blur, sharpen, greyscale, sepia, dither, mosaic, pixelate, dmc
from time import time
from copy import deepcopy

class Photoshop:
    """
    The main interface point for the image processing model.
    """
    def __init__(self):
        self.filename = None
        self.matrix = None
        self.modMatrix = None
        self.width = 0
        self.height = 0
        self.text = None
        self.legend = None

    def getImage(self):
        """
        Convert a 3d numpy matrix back into an image.
        """
        return util.getImage(self.modMatrix)
	
    def load(self, filename):
        """
        Load an image from a file on disk into the model.
        """
        if filename is None:
            raise TypeError("Filename is None")
        if filename.strip() == "":
            raise ValueError("Filename cannot be empty.")
        self.filename = filename
        self.matrix = util.readImage(filename)
        self.modMatrix = deepcopy(self.matrix)
        self.width = util.getWidth(self.matrix)
        self.height = util.getHeight(self.matrix)
	
    def save(self, filename):
        """
        Save an image from the model onto disk.
        """
        if filename is None:
            raise TypeError("Filename is None")
        # if extension is None:
        #     raise TypeError("Extension is None")
        util.writeImage(self.modMatrix, filename)

    def reset(self):
        """
        Reset an image back to the original image.
        """
        self.modMatrix = self.matrix
        self.text = None
        self.legend = None

    def blur(self, strength):
        """
        Apply a gaussian blur effect to the image.
        :param strength: The number of times to apply this filter.
        """
        self._checkStrength(strength)
        tempMatrix = deepcopy(self.modMatrix)
        blurWorker = blur.Blur()
        for _ in range(strength):
            tempMatrix = blurWorker.apply(tempMatrix)
        self.modMatrix = tempMatrix

    def sharpen(self, strength):
        """
        Apply a sharpen effect to the image where contrasting colors are accentuated.
        :param strength: The number of times to apply this filter.
        """
        self._checkStrength(strength)
        tempMatrix = deepcopy(self.modMatrix)
        sharpenWorker = sharpen.Sharpen()
        for _ in range(strength):
            tempMatrix = sharpenWorker.apply(tempMatrix)
        self.modMatrix = tempMatrix

    def greyscale(self, strength):
        """
        Apply a greyscale color effect to the image.
        :param strength: The number of times to apply this filter.
        """
        self._checkStrength(strength)
        tempMatrix = deepcopy(self.modMatrix)
        greyscaleWorker = greyscale.Greyscale()
        for _ in range(strength):
            tempMatrix = greyscaleWorker.apply(tempMatrix)
        self.modMatrix = tempMatrix

    def sepia(self, strength):
        """
        Apply a sepia color effect to the image.
        :param strength: The number of times to apply this filter.
        """
        self._checkStrength(strength)
        tempMatrix = deepcopy(self.modMatrix)
        sepiaWorker = sepia.Sepia()
        for _ in range(strength):
            tempMatrix = sepiaWorker.apply(tempMatrix)
        self.modMatrix = tempMatrix

    def dither(self, strength):
        """
        self._checkStrength(strength)
        Apply a floyd steinberg dither effect to the image.
        :param strength: The number of times to apply this filter.
        """
        tempMatrix = deepcopy(self.modMatrix)
        ditherWorker = dither.Dither()
        for _ in range(strength):
            tempMatrix = ditherWorker.apply(tempMatrix)
        self.modMatrix = tempMatrix

    def mosaic(self, numSeeds):
        """
        Apply a mosaic effect to the image.
        :param numSeeds: The number of random seeds to apply to this filter.
        """
        self._checkNumSeeds(numSeeds)
        tempMatrix = deepcopy(self.modMatrix)
        mosaicWorker = mosaic.Mosaic()
        tempMatrix = mosaicWorker.apply(tempMatrix, numSeeds)
        self.modMatrix = tempMatrix

    def pixelate(self, numSuperPixels):
        """
        Apply a pixelation effect to the image.
        :param numSeeds: The number of square superpixels to apply across the image.
        """
        tempMatrix = deepcopy(self.modMatrix)
        pixelateWorker = pixelate.Pixelate()
        tempMatrix = pixelateWorker.apply(tempMatrix, numSuperPixels)
        self.modMatrix = tempMatrix

    def dmcColor(self, numSuperPixels):
        """
        Convert all the colors to a DMC color palette.
        """
        tempMatrix = deepcopy(self.modMatrix)
        dmcWorker = dmc.Dmc()
        tempMatrix = dmcWorker.apply(tempMatrix, numSuperPixels)
        self.modMatrix = tempMatrix

    def _checkStrength(self, strength):
        if strength <= 0:
            raise ValueError("Error, strength cannot be less than 1")
        if strength > 99:
            raise ValueError("Error, strength cannot be greater than 99")

    def _checkNumSeeds(self, numSeeds):
        if numSeeds < 1:
            raise ValueError("Error, number of seeds cannot be less than 1")
        if numSeeds > (self.width * self.height):
            raise ValueError(f"Error, number of seeds cannot greater than \
            '{self.width * self.height}'")
