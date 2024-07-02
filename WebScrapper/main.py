import requests
from bs4 import BeautifulSoup
import concurrent.futures
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import re
import time
from matplotlib.ticker import MaxNLocator

def fetch_headlines(url):
    """
    Pobiera nagłówki artykułów ze strony internetowej podanej w URL.

    Argumenty:
    url (str): URL strony internetowej.

    Zwraca:
    tuple: Krotka zawierająca URL i pobrane nagłówki lub komunikat o błędzie.
    """
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = [headline.get_text().strip() for headline in soup.find_all('h3')]
        return url, headlines
    except Exception as e:
        return url, f"Error: {e}"
    
def plot_word_counts(word_counts, category):
    """
    Rysuje wykres słupkowy liczby słów dla danej kategorii.

    Argumenty:
    word_counts (Counter): Obiekt Counter z liczbą słów.
    category (str): Kategoria stron internetowych.
    """
    words, counts = zip(*word_counts.most_common(10))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(words, counts)
    ax.set_title(f"Najpopularniejsze słowa w kategorii {category}")
    ax.set_xlabel("Słowo")
    ax.set_ylabel("Ilość")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()

def main():
    websites = {
    "News": [
        "https://www.bbc.com","https://www.theguardian.com","https://www.aljazeera.com",
        "https://www.foxnews.com", "https://www.wsj.com"
    ],
    "Sports": [
        "https://www.espn.com","https://www.cbssports.com", "https://www.bleacherreport.com",
        "https://www.nbcsports.com", "https://www.si.com", "https://www.goal.com",
        "https://www.skysports.com"
    ],
    "Technology": [
        "https://www.techcrunch.com", "https://www.wired.com", "https://www.theverge.com",
        "https://www.cnet.com", "https://www.pcworld.com", "https://www.techradar.com",
        "https://www.tomshardware.com"
    ],
    "Entertainment": [
        "https://www.tmz.com", "https://www.variety.com", "https://www.rollingstone.com",
        "https://www.etonline.com", "https://www.hollywoodreporter.com","https://www.eonline.com",
        "https://www.vanityfair.com"
    ],
    "Science": [
        "https://www.sciencenews.org", "https://www.nature.com", "https://www.sciencemag.org",
        "https://www.newscientist.com", "https://www.livescience.com","https://www.smithsonianmag.com"
    ]
}

    headlines_by_category = defaultdict(list)
    word_counts_by_category = defaultdict(Counter)

    ignored_words = {'re','ri', 've', 'll', 'and', 'the', 'in', 'of', 'to', 'for', 'is', 'on', 'that', 'by', 'with', 'as', 'was',
                     'it', 'at', 'from', 'an', 'you', 'how', 'up', 'he','be','us','get','may','this','has','what','after','not',
                     'your','are','just','have','its','if','over','into','out','who','she','her','why','could','we','no','so'}


    start_time = time.time()

    headlines_limit_per_site = 15

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url_category = {
            executor.submit(fetch_headlines, url): (category, url)
            for category, urls in websites.items()
            for url in urls
        }
        for future in concurrent.futures.as_completed(future_to_url_category):
            category, url = future_to_url_category[future]
            try:
                url, headlines = future.result()
                for headline in headlines[:headlines_limit_per_site]:
                    headlines_by_category[category].append((url, headline))
                    words = re.findall(r'\w+', headline.lower())
                    filtered_words = [word for word in words if word not in ignored_words and len(word) > 1]
                    word_counts_by_category[category].update(filtered_words)
            except Exception as e:
                print(f"Error fetching headlines from {url}: {e}")

    end_time = time.time()
    print(f"Czas wykonania wielowątkowości: {end_time - start_time} sekund")

    for category, headlines in headlines_by_category.items():
        print(f"\nKategoria: {category}")
        for url, headline in headlines:
            print(f"  URL: {url}, Nagłówek: {headline}")

    for category, counts in word_counts_by_category.items():
        plot_word_counts(counts, category)

    plt.show()

if __name__ == "__main__":
    main()


    