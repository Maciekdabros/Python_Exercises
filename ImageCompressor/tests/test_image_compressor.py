import unittest
from model.compressor import ImageCompressor
from PIL import Image
import numpy as np

#python -m unittest discover -s tests

class TestImageCompressor(unittest.TestCase):
    """Testy dla klasy ImageCompressor sprawdzające poprawność algorytmów SVD."""
    def setUp(self):
        """Konfiguracja środowiska testowego przed każdym testem."""
        self.compressor = ImageCompressor()

    def test_svd_compress_grayscale(self):
        """
        Test sprawdzający, czy metoda svd_compress_grayscale kompresuje obraz w skali szarości
        i zwraca obiekt Image.
        """
        test_image = Image.fromarray(np.random.randint(0, 255, (10, 10), dtype=np.uint8))
        components = 5
        result = self.compressor.svd_compress_grayscale(test_image, components)
        self.assertIsInstance(result, Image.Image)

    def test_svd_compress_color(self):
        """
        Test sprawdzający, czy metoda svd_compress_color kompresuje obraz kolorowy
        i zwraca obiekt Image.
        """
        test_image = Image.fromarray(np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8))
        components = 5
        result = self.compressor.svd_compress_color(test_image, components)
        self.assertIsInstance(result, Image.Image)

if __name__ == '__main__':
    unittest.main()