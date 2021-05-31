from model import photoshop
import os
from PIL import Image

if __name__ == "__main__":
	ps1 = photoshop.Photoshop()
	path = '/Users/dennisping/Documents/image-processor-mvc/res/lowfi.jpg'
	#path = '/Users/dennisping/Documents/image-processor-mvc/res/city_nezuko_by_eternal_s.jpg'
	ps1.load(path)

	ps1.dither(1)
	myImage = ps1.getImage()
	myImage.show()