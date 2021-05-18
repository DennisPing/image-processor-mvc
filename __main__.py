from model import photoshop
import os
from PIL import Image

if __name__ == "__main__":
    ps1 = photoshop.Photoshop()
    path = '/Users/dennisping/image-processor-mvc/res/lowfi.jpg'
    #path = None
    ps1.load(path)

    ps1.mosaic(1000)
    myImage = ps1.getImage()
    myImage.show()