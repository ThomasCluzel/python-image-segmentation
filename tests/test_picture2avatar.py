# To import from parent folder
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pytest

from picture2avatar import main, Image


class TestAlgorithms:
    """Test class for the module picture2avatar

    This class contains all methods to test the algorithms
    to process a picture available in the picture2avatar module.
    """
    @classmethod
    def setup_class(cls):
        """Initialisation for the tests
        """
        cls.INPUT_PATH = "img.png"
        cls.OUTPUT_PATH = "img-result.png"
        test_picture = Image.new("RGB", (2, 2))
        test_picture.putpixel((0, 0), (0, 0, 0))
        test_picture.putpixel((0, 1), (20, 20, 20))
        test_picture.putpixel((1, 0), (250, 250, 250))
        test_picture.putpixel((1, 1), (255, 255, 255))
        test_picture.save(cls.INPUT_PATH)

    def test_pre(self):
        """Test the threshold algorithm
        """
        main(self.INPUT_PATH, "pre", self.OUTPUT_PATH, 1)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (0, 0, 0)
        assert res.getpixel((0, 1)) == (0, 0, 0)
        assert res.getpixel((1, 0)) == (128, 128, 128)
        assert res.getpixel((1, 1)) == (128, 128, 128)

    def test_grow1(self):
        """Test the region growth algorithm
        """
        main(self.INPUT_PATH, "grow", self.OUTPUT_PATH, 1)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (0, 0, 0)
        assert res.getpixel((0, 1)) == (20, 20, 20)
        assert res.getpixel((1, 0)) == (250, 250, 250)
        assert res.getpixel((1, 1)) == (255, 255, 255)

    def test_grow2(self):
        """Test the region growth algorithm
        """
        main(self.INPUT_PATH, "grow", self.OUTPUT_PATH, 10)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (0, 0, 0)
        assert res.getpixel((0, 1)) == (20, 20, 20)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_grow3(self):
        """Test the region growth algorithm
        """
        main(self.INPUT_PATH, "grow", self.OUTPUT_PATH, 25)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (10, 10, 10)
        assert res.getpixel((0, 1)) == (10, 10, 10)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_clu(self):
        """Test the clustering algorithm
        """
        main(self.INPUT_PATH, "clu", self.OUTPUT_PATH, 2)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (10, 10, 10)
        assert res.getpixel((0, 1)) == (10, 10, 10)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_greed1(self):
        """Test the greedy algorithm
        """
        main(self.INPUT_PATH, "greed", self.OUTPUT_PATH, 4)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (10, 10, 10)  # because greedy
        assert res.getpixel((0, 1)) == (10, 10, 10)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_greed2(self):
        """Test the greedy algorithm
        """
        main(self.INPUT_PATH, "greed", self.OUTPUT_PATH, 3)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (10, 10, 10)  # because greedy
        assert res.getpixel((0, 1)) == (10, 10, 10)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_greed3(self):
        """Test the greedy algorithm
        """
        main(self.INPUT_PATH, "greed", self.OUTPUT_PATH, 2)
        res = Image.open(self.OUTPUT_PATH)
        assert res.getpixel((0, 0)) == (10, 10, 10)
        assert res.getpixel((0, 1)) == (10, 10, 10)
        assert res.getpixel((1, 0)) == (252, 252, 252)
        assert res.getpixel((1, 1)) == (252, 252, 252)

    def test_message_unknown_algorithm(self, capfd):
        """Tests correct output
        """
        with pytest.raises(ValueError):
            main(self.INPUT_PATH, "unknown")

    def test_exception_file_does_not_exist(self, capfd):
        """Tests correct output
        """
        with pytest.raises(IOError):
            main("unknownfile.unk", "pre")

    @classmethod
    def teardown_class(cls):
        """Delete generated files
        """
        os.remove(cls.INPUT_PATH)
        os.remove(cls.OUTPUT_PATH)
