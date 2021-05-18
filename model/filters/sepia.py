import numpy as np
from model.filters.dotproduct import DotProduct

class Sepia(DotProduct):

	def __init__(self):
		pass

	def apply(self, matrix):
		kernel = np.array([[0.393, 0.769, 0.189],
							[0.349, 0.686, 0.168],
							[0.272, 0.534, 0.131]])

		return self.fast_dotproduct(matrix, kernel)