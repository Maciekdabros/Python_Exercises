from datetime import datetime

class Zadanie:
    def __init__(self, tytul, opis, termin_wykonania, wykonane=False):
        self.tytul = tytul
        self.opis = opis
        self.termin_wykonania = termin_wykonania
        self.wykonane = wykonane
    
    def __str__(self):
        return f"{self.tytul}, {self.opis}, do {self.termin_wykonania}, Wykonane: {self.wykonane}"
    
class ZadaniePriorytetowe(Zadanie):
    def __init__(self, tytul, opis, termin_wykonania, priorytet, wykonane=False):
        Zadanie.__init__(self, tytul, opis, termin_wykonania, wykonane)
        self.priorytet = priorytet
    
    def __str__(self):
        return f"{Zadanie.__str__(self)}, Priorytet: {self.priorytet}"

class ZadanieRegularne(Zadanie):
    def __init__(self, tytul, opis, termin_wykonania, powtarzalnosc, wykonane=False):
        Zadanie.__init__(self, tytul, opis, termin_wykonania, wykonane)
        self.powtarzalnosc = powtarzalnosc
    
    def __str__(self):
        return f"{Zadanie.__str__(self)}, Powtarzalność: {self.powtarzalnosc}"

class ManagerZadan:
    def __init__(self):
        self.zadania = []
    
    def dodaj_zadanie(self, zadanie):
        self.zadania.append(zadanie)
    
    def usun_zadanie(self, tytul):
        if tytul in self: 
            zadanie_do_usuniecia = next((z for z in self.zadania if z.tytul == tytul), None)
            self.zadania.remove(zadanie_do_usuniecia)
        else:
            print("Podane zadanie nie istnieje")

    def oznacz_jako_wykonane(self, tytul):
        zadanie_do_oznaczenia = next((z for z in self.zadania if z.tytul == tytul), None)
        if zadanie_do_oznaczenia is not None:
            zadanie_do_oznaczenia.wykonane = True
        else:
            print("Podane zadanie nie istnieje")

    def edytuj_zadanie(self, stary_tytul, nowy_tytul, nowy_opis, nowy_termin):
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
        return any(z.tytul == tytul for z in self.zadania)
    
    def wyswietl_zadania(self):
        if not self.zadania:
            print("Brak zadań do wyświetlenia.")
        else:
            for zadanie in self.zadania:
                print(zadanie)

    def sortuj_zadania(self):
        self.zadania.sort(key=lambda x: x.termin_wykonania)
    
manager = ManagerZadan()

while True:
    print("\n1. Dodaj zadanie")
    print("2. Usuń zadanie")
    print("3. Oznacz zadanie jako wykonane")
    print("4. Edytuj zadanie")
    print("5. Wyświetl wszystkie zadania")
    print("6. Sortuj zadania po terminie")
    print("7. Wyjście")
    
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
            zadanie = ZadanieRegularne(tytul, opis, termin, powtarzalnosc)
        elif typ_zadania.upper() == "P":
            priorytet = int(input("Podaj priorytet zadania (liczba): "))
            zadanie = ZadaniePriorytetowe(tytul, opis, termin, priorytet)
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
        break
    else:
        print("Nieznana opcja")


