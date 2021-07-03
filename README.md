# image-processor-mvc

A python implementation of a basic image processing program.

The point of this project is to learn Python by redo-ing my old Java homework. This old homework is a complete MVC program that can edit images.

## My goals for this project

1. To implement an Image Processing MVC program using Python and popular modules:
    - numpy
    - scipy
    - Pillow
2. To learn Python specific design patterns
3. To practice general design patterns
4. To learn PyQT5

## What this project is not

1. Not compact, efficient code:
    - I purposely chose to do tasks manually in order to practice Python fundamentals.
2. Not pure object oriented programming
    - Python gives me some flexibility:
    - Because Python is fundamentally slow, I need to find ways to gain performance.
3. Not pure functional programming:
    - I still want to practice OOP wherever applicable.

## Python and Pip requirements

- Python 3
- numpy
- numba
- scipy
- Pillow
- PyQt5

## Features that are working

- [x] Gaussian Blur
- [x] Sharpen
- [x] Greyscale Color
- [x] Sepia Color
- [x] Mosaic
- [x] Pixelate
- [x] Floyd Steinberg Dithering

## To-do

- [ ] Controller
- [ ] View
- [ ] Testing with PyTest
- [ ] Add GIF support
- [ ] Add Rotate feature
- [ ] Add Grain filter feature

## Supported input image formats

- PNG
- JPG
