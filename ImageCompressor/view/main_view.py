import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class MainView(tk.Tk):
    """
    Główny widok interfejsu użytkownika dla aplikacji kompresji obrazów.
    
    Metody:
        on_open_image: Otwiera dialog wyboru pliku do załadowania obrazu.
        show_image: Wyświetla obraz w interfejsie użytkownika.
        on_compress: Inicjuje proces kompresji obrazu.
        show_error: Wyświetla komunikat o błędzie.
    """
    def __init__(self, presenter):
        """
        Inicjalizuje widok z danym prezenterem.
        
        Parametry:
            presenter (MainPresenter): Prezenter obsługujący logikę aplikacji.
        """
        super().__init__()
        self.presenter = presenter
        self.title("Image Compressor")
        self.geometry("800x600")

        self.open_button = tk.Button(self, text="Open Image", command=self.on_open_image)
        self.open_button.pack()

        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.label_r = tk.Label(self, text="Liczba wartości osobliwych:")
        self.label_r.pack()

        self.entry_r = tk.Entry(self)
        self.entry_r.pack()

        self.compress_option = tk.StringVar(value="color")

        self.radio_color = ttk.Radiobutton(self, text="Kompresja kolorowa", variable=self.compress_option, value="color")
        self.radio_color.pack()

        self.radio_grayscale = ttk.Radiobutton(self, text="Kompresja szarości", variable=self.compress_option, value="grayscale")
        self.radio_grayscale.pack()


        self.compress_button = tk.Button(self, text="Kompresuj obraz", command=self.on_compress)
        self.compress_button.pack()

    def on_open_image(self):
        """
        Wywoływana, aby otworzyć dialog wyboru pliku i załadować obraz do aplikacji.
        
        Używa filedialog z biblioteki tkinter, aby umożliwić użytkownikowi wybór pliku obrazu.
        Obsługiwane formaty to JPG, BMP i PNG.
        Po wybraniu pliku, ścieżka jest przekazywana do metody load_image prezentatora.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.bmp;*.png")]
        )
        if filepath:
            self.presenter.load_image(filepath)

    def show_image(self, image):
        """
        Wyświetla podany obraz w interfejsie użytkownika.
        
        Obraz jest skalowany do maksymalnej szerokości i wysokości, zachowując proporcje.
        Skalowany obraz jest następnie konwertowany na PhotoImage i wyświetlany w etykiecie.
        
        Parametry:
            image (Image.Image): Obraz, który ma być wyświetlony.
        """
        max_height = 500
        max_width = 500

        original_width, original_height = image.size

        scale = min(max_width/original_width, max_height/original_height)

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        photo_image = ImageTk.PhotoImage(resized_image)

        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image

    def set_presenter(self, presenter):
        """
        Ustawia prezentera dla widoku.
        
        Parametry:
            presenter (MainPresenter): Prezenter do obsługi logiki aplikacji.
        """
        self.presenter = presenter

    def on_compress(self):
        """
        Wywoływana po naciśnięciu przycisku kompresji obrazu.
        
        Pobiera wartość r (liczba wartości osobliwych) z pola tekstowego.
        Jeśli wartość jest liczbą, przekazuje ją do metody compress_image prezentatora.
        W przeciwnym razie wyświetla okno dialogowe z błędem.
        """
        r_value = self.entry_r.get()
        if r_value.isdigit():
            self.presenter.compress_image(int(r_value), self.compress_option.get())
        else:
            tk.messagebox.showerror("Błąd", "Proszę wprowadzić wartość liczbową dla r.")

    def show_error(self, message):
        """
        Wyświetla okno dialogowe z błędem zawierającym podaną wiadomość.
        
        Parametry:
            message (str): Wiadomość błędu do wyświetlenia użytkownikowi.
        """
        tk.messagebox.showerror("Błąd", message)