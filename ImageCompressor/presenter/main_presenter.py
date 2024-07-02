from view.main_view import MainView
from model.compressor import ImageCompressor
from PIL import Image

class MainPresenter:
    """
    Prezenter obsługujący główne działania w interfejsie użytkownika aplikacji kompresji obrazów.
    
    Metody:
        compress_image: Kompresuje obraz za pomocą metody SVD.
        load_image: Ładuje obraz z dysku.
    """
    
    def __init__(self, view):
        """
        Inicjalizuje prezentera z danym widokiem.
        
        Parametry:
            view (MainView): Instancja widoku do obsługi interakcji z użytkownikiem.
        """   
        self.view = view
        self.model = ImageCompressor()
        self.current_image = None

    def compress_image(self, r, option):
        """
        Kompresuje aktualny obraz przy użyciu SVD, z wyborem na obraz kolorowy lub szarości.
        
        Parametry:
            r (int): Liczba wartości osobliwych do użycia w kompresji.
            option (str): Typ kompresji do zastosowania ("color" lub "grayscale").
        
        Wyjątki:
            Wyświetla błąd w widoku, jeśli kompresja się nie powiedzie.
        """
        if self.current_image:
            try:
                if option == "color":
                    compressed_image = self.model.svd_compress_color(self.current_image, r)
                elif option == "grayscale":
                    grayscale_image = self.current_image.convert('L')
                    compressed_image = self.model.svd_compress_grayscale(grayscale_image, r)
                self.view.show_image(compressed_image)
            except Exception as e:
                self.view.show_error(f"Błąd podczas kompresji obrazu: {e}")
        else:
            self.view.show_error("Błąd: Obraz nie został załadowany prawidłowo.")

    def load_image(self, filepath):
        """
        Ładuje obraz do aplikacji z podanej ścieżki pliku.
        
        Parametry:
            filepath (str): Ścieżka do pliku obrazu do załadowania.
        
        Wyjątki:
            Wyświetla błąd w widoku, jeśli załadowanie się nie powiedzie.
        """
        try:
            image = Image.open(filepath)
            self.current_image = image
            self.view.show_image(image)
        except Exception as e:
            self.view.show_error(f"Błąd podczas ładowania obrazu: {e}")

if __name__ == "__main__":
    view = MainView(MainPresenter)
    presenter = MainPresenter(view)
    view.mainloop()