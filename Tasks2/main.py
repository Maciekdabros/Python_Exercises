"""
Moduł do zarządzania zadaniami.

Ten moduł zawiera klasy do tworzenia i zarządzania zadaniami. Umożliwia dodawanie, usuwanie, edycję oraz zapisywanie i wczytywanie zadań z pliku.
"""

from datetime import datetime
import time

class Zadanie:
    """
    Klasa reprezentująca pojedyncze zadanie.
    """
    def __init__(self, tytul, opis, termin_wykonania, wykonane=False, **kwargs):
        """
        Inicjalizacja zadania.

        :param tytul: Tytuł zadania.1
        :param opis: Opis zadania.
        :param termin_wykonania: Termin wykonania zadania.
        :param wykonane: Czy zadanie zostało wykonane.
        :param kwargs: Dodatkowe informacje o zadaniu.
        """
        self.tytul = tytul
        self.opis = opis
        self.termin_wykonania = termin_wykonania
        self.wykonane = wykonane
        self.dodatkowe_info = kwargs

    def __str__(self):
        """
        Reprezentacja tekstowa zadania.

        :return: Tekstowa reprezentacja zadania.
        """
        dodatkowe = ', '.join(f"{k}: {v}" for k, v in self.dodatkowe_info.items())
        return f"{self.tytul}, {self.opis}, {self.termin_wykonania}, Wykonane: {self.wykonane}" + (f", {dodatkowe}" if dodatkowe else "")
    
class ZadaniePriorytetowe(Zadanie):
    """
    Klasa reprezentująca zadanie z priorytetem.
    """
    def __init__(self, tytul, opis, termin_wykonania, wykonane=False, priorytet=1, **kwargs):
        """
        Inicjalizacja zadania z priorytetem.

        :param tytul: Tytuł zadania.
        :param opis: Opis zadania.
        :param termin_wykonania: Termin wykonania zadania.
        :param wykonane: Czy zadanie zostało wykonane.
        :param priorytet: Priorytet zadania.
        :param kwargs: Dodatkowe informacje o zadaniu.
        """
        super().__init__(tytul, opis, termin_wykonania, wykonane, **kwargs)
        self.priorytet = priorytet
    
    def __str__(self):
        """
        Reprezentacja tekstowa zadania z priorytetem.

        :return: Tekstowa reprezentacja zadania z priorytetem.
        """
        return f"{Zadanie.__str__(self)}, Priorytet: {self.priorytet}"

class ZadanieRegularne(Zadanie):
    """
    Klasa reprezentująca regularne zadanie, które może być powtarzalne.
    """
    def __init__(self, tytul, opis, termin_wykonania, wykonane=False, powtarzalnosc=False, **kwargs):
        """
        Inicjalizacja regularnego zadania.

        :param tytul: Tytuł zadania.
        :param opis: Opis zadania.
        :param termin_wykonania: Termin wykonania zadania.
        :param wykonane: Czy zadanie zostało wykonane.
        :param powtarzalnosc: Czy zadanie jest powtarzalne.
        :param kwargs: Dodatkowe informacje o zadaniu.
        """
        super().__init__(tytul, opis, termin_wykonania, wykonane, **kwargs)
        self.powtarzalnosc = powtarzalnosc
    
    def __str__(self):
        """
        Reprezentacja tekstowa regularnego zadania.

        :return: Tekstowa reprezentacja regularnego zadania.
        """
        return f"{Zadanie.__str__(self)}, Powtarzalnosc: {self.powtarzalnosc}"

class ManagerZadan:
    """
    Klasa do zarządzania zadaniami.
    """
    def __init__(self):
        """
        Inicjalizacja managera zadań.
        """
        self.zadania = []
    
    def dodaj_zadanie(self, zadanie):
        """
        Dodaje zadanie do listy zadań.

        :param zadanie: Obiekt zadania do dodania.
        """
        self.zadania.append(zadanie)
    
    def usun_zadanie(self, tytul):
        """
        Usuwa zadanie na podstawie tytułu.

        :param tytul: Tytuł zadania do usunięcia.
        """
        if tytul in self: 
            zadanie_do_usuniecia = next((z for z in self.zadania if z.tytul == tytul), None)
            self.zadania.remove(zadanie_do_usuniecia)
        else:
            print("Podane zadanie nie istnieje")

    def oznacz_jako_wykonane(self, tytul):
        """
        Oznacza zadanie jako wykonane na podstawie tytułu.

        :param tytul: Tytuł zadania do oznaczenia.
        """
        zadanie_do_oznaczenia = next((z for z in self.zadania if z.tytul == tytul), None)
        if zadanie_do_oznaczenia is not None:
            zadanie_do_oznaczenia.wykonane = True
        else:
            print("Podane zadanie nie istnieje")

    def edytuj_zadanie(self, stary_tytul, nowy_tytul, nowy_opis, nowy_termin):
        """
        Edytuje zadanie na podstawie tytułu.

        :param stary_tytul: Stary tytuł zadania.
        :param nowy_tytul: Nowy tytuł zadania.
        :param nowy_opis: Nowy opis zadania.
        :param nowy_termin: Nowy termin wykonania zadania.
        :return: True jeśli edycja się powiodła, False w przeciwnym razie.
        """
        zadanie_do_edytowania = next((z for z in self.zadania if z.tytul == stary_tytul), None)
        if zadanie_do_edytowania is not None:
            zadanie_do_edytowania.tytul = nowy_tytul
            zadanie_do_edytowania.opis = nowy_opis
            zadanie_do_edytowania.termin_wykonania = nowy_termin
            return True
        else:
            print("Podane zadanie nie istnieje")
            return False
    def __contains__(self, tytul):
        """
        Sprawdza, czy zadanie o podanym tytule istnieje w managerze.

        :param tytul: Tytuł zadania.
        :return: True jeśli zadanie istnieje, False w przeciwnym razie.
        """
        return any(z.tytul == tytul for z in self.zadania)
    
    def wyswietl_zadania(self):
        """
        Wyświetla wszystkie zadania.
        """
        if not self.zadania:
            print("Brak zadań do wyświetlenia.")
        else:
            for zadanie in self.zadania:
                print(zadanie)

    def pomiar_czasu(funkcja):
        """
        Dekorator mierzący czas wykonania funkcji.

        :param funkcja: Funkcja, której czas wykonania ma być zmierzony.
        :return: Wynik działania funkcji.
        """
        def zmierz_czas(*args, **kwargs):
            start = time.time()
            wynik = funkcja(*args, **kwargs)
            koniec = time.time()
            print(f"Czas wykonania {funkcja.__name__}: {koniec - start} sekund")
            return wynik
        return zmierz_czas
    

    @pomiar_czasu
    def sortuj_zadania(self):
        """
        Sortuje zadania na podstawie terminu wykonania.
        """
        self.zadania.sort(key=lambda x: x.termin_wykonania)


    def zapisz_do_pliku(self, nazwa_pliku=None):
        """
        Zapisuje zadania do pliku.

        :param nazwa_pliku: Nazwa pliku do zapisu. Domyślnie 'zadania.txt'.
        """
        if not nazwa_pliku:
            nazwa_pliku = input("Podaj nazwę pliku do zapisu (domyślnie 'zadania.txt'): ")
            if not nazwa_pliku:
                nazwa_pliku = "zadania.txt"
        
        @ManagerZadan.pomiar_czasu
        def zapisz():
            with open(nazwa_pliku, "w") as plik:
                for zadanie in self.zadania:
                    plik.write(str(zadanie) + "\n")
        
        zapisz()
        print(f"Zadania zapisane w pliku {nazwa_pliku}.")

    def wczytaj_z_pliku(self, nazwa_pliku=None):
        """
        Wczytuje zadania z pliku.

        :param nazwa_pliku: Nazwa pliku do odczytu. Domyślnie 'zadania.txt'.
        """
        if not nazwa_pliku:
            nazwa_pliku = input("Podaj nazwę pliku do odczytu (domyślnie 'zadania.txt'): ")
            if not nazwa_pliku:
                nazwa_pliku = "zadania.txt"
        
        @ManagerZadan.pomiar_czasu
        def wczytaj():
            try:
                with open(nazwa_pliku, "r") as plik:
                    for linia in plik:
                        elementy = linia.strip().split(', ')
                        tytul, opis, termin, wykonane = elementy[:4]
                        wykonane = wykonane.split(": ")[1] == "True"
                        dodatkowe = {}

                        for info in elementy[4:]:
                            klucz, wartosc = info.split(": ")
                            dodatkowe[klucz] = wartosc

                        if "Priorytet" in dodatkowe:
                            priorytet = int(dodatkowe.pop("Priorytet"))
                            zadanie = ZadaniePriorytetowe(tytul, opis, termin, wykonane, priorytet, **dodatkowe)
                        elif "Powtarzalnosc" in dodatkowe:
                            powtarzalnosc = dodatkowe.pop("Powtarzalnosc") == "True"
                            zadanie = ZadanieRegularne(tytul, opis, termin, wykonane, powtarzalnosc, **dodatkowe)
                        else:
                            zadanie = Zadanie(tytul, opis, termin, wykonane, **dodatkowe)

                        self.zadania.append(zadanie)
                print(f"Zadania wczytane z pliku {nazwa_pliku}.")
            except FileNotFoundError:
                print(f"Plik {nazwa_pliku} nie istnieje.")
        
        wczytaj()

manager = ManagerZadan()

if __name__ == "__main__":
    while True:
        print("\n1. Dodaj zadanie")
        print("2. Usuń zadanie")
        print("3. Oznacz zadanie jako wykonane")
        print("4. Edytuj zadanie")
        print("5. Wyświetl wszystkie zadania")
        print("6. Sortuj zadania po terminie")
        print("7. Zapisz zadania do pliku")
        print("8. Wczytaj zadania z pliku")
        print("9. Wyjście")
        
        wybor = input("\nWybierz opcję: ")
        
        if wybor == "1":
            tytul = input("Tytuł: ")
            opis = input("Opis: ")
            while True:
                termin = input("Termin wykonania (RRRR-MM-DD): ")
                try:
                    datetime.strptime(termin, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Niepoprawny format daty")

            dodatkowe = {}
            while True:
                klucz = input("Podaj klucz dodatkowej informacji (lub 'koniec', aby zakończyć): ")
                if klucz == "koniec":
                    break
                wartosc = input(f"Podaj wartość dla {klucz}: ")
                dodatkowe[klucz] = wartosc

            typ_zadania = input("Zadanie standardowe czy priorytetowe? [S/P]: ")
            if typ_zadania.upper() == "S":
                powtarzalnosc = input("Czy zadanie jest powtarzalne? [T/N]: ")
                if powtarzalnosc.upper() == "T":
                    powtarzalnosc = True
                elif powtarzalnosc.upper() == "N":
                    powtarzalnosc = False
                else:
                    print("Niepoprawny wybór")
                    continue
                zadanie = ZadanieRegularne(tytul, opis, termin, powtarzalnosc, **dodatkowe)
            elif typ_zadania.upper() == "P":
                priorytet = int(input("Podaj priorytet zadania (liczba): "))
                zadanie = ZadaniePriorytetowe(tytul, opis, termin, priorytet, **dodatkowe)
            else:
                print("Nieznany typ zadania")
                continue

            manager.dodaj_zadanie(zadanie)
        elif wybor == "2":
            tytul = input("Tytuł zadania do usunięcia: ")
            manager.usun_zadanie(tytul)
        elif wybor == "3":
            tytul = input("Tytuł zadania do oznaczenia: ")
            manager.oznacz_jako_wykonane(tytul)
        elif wybor == "4":
            stary_tytul = input("Tytuł zadania do edycji: ")
            nowy_tytul = input("Nowy tytuł: ")
            nowy_opis = input("Nowy opis: ")
            nowy_termin = input("Nowy termin wykonania: ")
            if manager.edytuj_zadanie(stary_tytul, nowy_tytul, nowy_opis, nowy_termin):
                print("Zadanie zaktualizowane.")
            else:
                print("Nie ma zadania o podanym tytule.")       
        elif wybor == "5":
            manager.wyswietl_zadania()
        elif wybor == "6":
            manager.sortuj_zadania()
            print("Zadania zostały posortowane.")
        elif wybor == "7":
            manager.zapisz_do_pliku()
        elif wybor == "8":
            manager.wczytaj_z_pliku()
        elif wybor == "9":
            break
        else:
            print("Nieznana opcja")


