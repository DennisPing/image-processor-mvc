from model import photoshop
import os
from PIL import Image

if __name__ == "__main__":
    ps1 = photoshop.Photoshop()
    #path = '/Users/dennisping/Documents/image-processor-mvc/res/lowfi.jpg'
    #path = '/Users/dennisping/Documents/image-processor-mvc/res/city_nezuko_by_eternal_s.jpg'
    path = '/Users/dennisping/Documents/image-processor-mvc/res/kda-nightmarket-720.png'
    #path = '/Users/dennisping/Documents/image-processor-mvc/res/kda-nightmarket-1080.png'
    #path = '/Users/dennisping/Documents/image-processor-mvc/res/Jiufen.png'
    ps1.load(path)

    ps1.dmcColor(100)
    myImage = ps1.getImage()
    myImage.show()