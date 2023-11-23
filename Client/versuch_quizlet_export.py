import requests
from bs4 import BeautifulSoup


def hole_quizlet_begriffsdefinitionen(quizlet_url):
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'yourcookie',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36',
        }

        antwort = requests.get(quizlet_url, headers=headers)
        if antwort.status_code == 200:
            suppe = BeautifulSoup(antwort.text, 'html.parser')
            begriffsdefinitionen = []

            for karte in suppe.find_all('div', class_='SetPage-term'):
                begriff = karte.find('span', class_='TermText').text.strip()
                definition = karte.find('span', class_='TermDefinition').text.strip()
                begriffsdefinitionen.append((begriff, definition))

            return begriffsdefinitionen
        else:
            print(f"Fehler beim Abrufen der Seite. Statuscode: {antwort.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")

    return []


if __name__ == '__main__':
    quizlet_url = input("Geben Sie den Link zum Quizlet-Set ein: ")
    begriffsdefinitionen = hole_quizlet_begriffsdefinitionen(quizlet_url)

    if begriffsdefinitionen:
        for index, (begriff, definition) in enumerate(begriffsdefinitionen, 1):
            print(f"{index}. Begriff: {begriff}\n   Definition: {definition}")
    else:
        print("Keine Begriff/Definition-Paare gefunden.")
