import numpy as np
from PIL import Image

class ImageCompressor:
    """
    Klasa do kompresji obrazów przy użyciu metody SVD.

    Metody:
        svd_compress_grayscale: Kompresuje obraz w skali szarości.
        svd_compress_color: Kompresuje obraz kolorowy.
    """
    def svd_compress_grayscale(self, image, components):
        """
        Kompresuje obraz w skali szarości przy użyciu SVD.
        
        Parametry:
            image (Image.Image): Obraz w skali szarości do kompresji.
            components (int): Liczba wartości osobliwych do użycia w kompresji.
        
        Zwraca:
            Image.Image: Skompresowany obraz w skali szarości.
        
        Wyjątki:
            Exception: W przypadku błędu kompresji.
        """
        try:

            image_matrix = np.array(image)
            U, s, Vt = np.linalg.svd(image_matrix, full_matrices=False)
            S = np.diag(s[:components])
            U = U[:, :components]
            Vt = Vt[:components, :]
            compressed_matrix = np.dot(U, np.dot(S, Vt))
            compressed_matrix = np.clip(compressed_matrix, 0, 255)
            compressed_image = Image.fromarray(compressed_matrix.astype('uint8'))

            return compressed_image
        except Exception as e:
            raise Exception(f"Błąd podczas kompresji obrazu w skali szarości: {e}")

    def svd_compress_color(self, image, components):
        """
        Kompresuje obraz kolorowy przy użyciu SVD.

        Parametry:
            image (Image.Image): Obraz do kompresji.
            components (int): Liczba wartości osobliwych do użycia w kompresji.

        Zwraca:
            Image.Image: Skompresowany obraz kolorowy.

        Wyjątki:
            Exception: W przypadku błędu kompresji.
        """
        image_array = np.array(image)
        channels_compressed = []
        for i in range(3):
            channel = image_array[:,:,i]
            U, s, Vt = np.linalg.svd(channel, full_matrices=False)
            S = np.diag(s[:components])
            U = U[:, :components]
            Vt = Vt[:components, :]
            compressed_channel = np.dot(U, np.dot(S, Vt))
            channels_compressed.append(compressed_channel)
            
        compressed_image = np.stack(channels_compressed, axis=-1)
        compressed_image = np.clip(compressed_image, 0, 255).astype('uint8')
        return Image.fromarray(compressed_image)
