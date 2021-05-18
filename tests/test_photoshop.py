import pytest
import numpy as np
from model import photoshop
from model import util

class TestModel:

    def test_valid_file(self):
        filename = '/Users/dennisping/image-processor-mvc/res/lowfi.jpg'
        ps = photoshop.Photoshop()
        ps.load(filename)
        assert ps.filename == '/Users/dennisping/image-processor-mvc/res/lowfi.jpg'
    
    def test_load_none_file(self):
        with pytest.raises(TypeError):
            filename = None
            ps = photoshop.Photoshop()
            ps.load(filename)

    def test_load_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            filename = "wrongname"
            ps = photoshop.Photoshop()
            ps.load(filename)

    def test_copy_matrix_mock(self):
        matrix = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        copyMatrix = util.makeCopy(matrix)
        np.testing.assert_array_equal(copyMatrix, matrix)

    def test_copy_matrix_actual(self):
        filename = '/Users/dennisping/image-processor-mvc/res/lowfi.jpg'
        ps = photoshop.Photoshop()
        ps.load(filename)
        copyMatrix = util.makeCopy(ps.matrix)
        np.testing.assert_array_equal(copyMatrix, ps.matrix)
        

            
        

    