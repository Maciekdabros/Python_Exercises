from view.main_view import MainView
from presenter.main_presenter import MainPresenter

def main():
    """
    Funkcja główna uruchamiająca aplikację kompresji obrazów.
    """
    view = MainView(None)
    presenter = MainPresenter(view)
    view.set_presenter(presenter)
    view.mainloop()
    

if __name__ == '__main__':
    main()
