from model import util
import numpy as np
import copy
from model.filters import blur, sharpen, greyscale, sepia, dither, mosaic, pixelate
from time import time
from copy import deepcopy

class Photoshop:
	def __init__(self, filename = None, matrix = None, modMatrix = None, width = 0, height = 0, text = None, legend = None):
		self.filename = filename
		self.matrix = matrix
		self.modMatrix = modMatrix
		self.width = width
		self.height = height
		self.text = text
		self.legend = legend

	def getImage(self):
		return util.getImage(self.modMatrix)
	
	def load(self, filename):
		if filename is None:
			raise TypeError("Filename is None")
		if filename.strip() == "":
			raise ValueError("Filename cannot be empty.")
		self.filename = filename
		self.matrix = util.readImage(filename)
		self.modMatrix = util.makeCopy(self.matrix)
		self.width = util.getWidth(self.matrix)
		self.height = util.getHeight(self.matrix)
	
	def save(self, filename):
		if filename is None:
			raise TypeError("Filename is None")
		# if extension is None:
		#     raise TypeError("Extension is None")
		util.writeImage(self.modMatrix, filename)

	def reset(self):
		self.modMatrix = self.matrix
		self.text = None
		self.legend = None

	def blur(self, strength):
		#tempMatrix = util.makeCopy(self.modMatrix)
		tempMatrix = deepcopy(self.modMatrix)
		blurWorker = blur.Blur()
		for _ in range(strength):
			tempMatrix = blurWorker.apply(tempMatrix)
		self.modMatrix = tempMatrix
	
	def sharpen(self, strength):
		tempMatrix = deepcopy(self.modMatrix)
		sharpenWorker = sharpen.Sharpen()
		for _ in range(strength):
			tempMatrix = sharpenWorker.apply(tempMatrix)
		self.modMatrix = tempMatrix

	def greyscale(self, strength):
		tempMatrix = deepcopy(self.modMatrix)
		greyscaleWorker = greyscale.Greyscale()
		for _ in range(strength):
			tempMatrix = greyscaleWorker.apply(tempMatrix)
		self.modMatrix = tempMatrix

	def sepia(self, strength):
		tempMatrix = deepcopy(self.modMatrix)
		sepiaWorker = sepia.Sepia()
		for _ in range(strength):
			tempMatrix = sepiaWorker.apply(tempMatrix)
		self.modMatrix = tempMatrix

	def dither(self, strength):
		tempMatrix = deepcopy(self.modMatrix)
		ditherWorker = dither.Dither()
		for _ in range(strength):
			tempMatrix = ditherWorker.apply(tempMatrix)
		self.modMatrix = tempMatrix

	def mosaic(self, numSeeds):
		tempMatrix = deepcopy(self.modMatrix)
		mosaicWorker = mosaic.Mosaic()
		tempMatrix = mosaicWorker.apply(tempMatrix, numSeeds)
		self.modMatrix = tempMatrix

	def pixelate(self, numSeeds):
		tempMatrix = deepcopy(self.modMatrix)
		pixelateWorker = pixelate.Pixelate()
		tempMatrix = pixelateWorker.apply(tempMatrix, numSeeds)
		self.modMatrix = tempMatrix

