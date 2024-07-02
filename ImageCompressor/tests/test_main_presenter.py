import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from presenter.main_presenter import MainPresenter
from view.main_view import MainView
import unittest
from unittest.mock import patch, Mock
from PIL import Image

class TestMainPresenter(unittest.TestCase):
    """Testy dla klasy MainPresenter sprawdzające logikę prezentacji danych."""

    def setUp(self):
        """Konfiguracja mocków i środowiska testowego przed każdym testem."""
        self.view = Mock(spec=MainView)
        self.presenter = MainPresenter(self.view)

    @patch('presenter.main_presenter.Image.open')
    def test_load_image(self, mock_open):
        """
        Test sprawdzający, czy metoda load_image prawidłowo otwiera obraz
        i wywołuje odpowiednią metodę wyświetlania w widoku.
        """
        mock_image = Mock(spec=Image.Image)
        mock_open.return_value = mock_image
        fake_path = 'fake/path/to/image.jpg'
        self.presenter.load_image(fake_path)
        mock_open.assert_called_with(fake_path)
        self.view.show_image.assert_called_with(mock_image)

if __name__ == '__main__':
    unittest.main()
