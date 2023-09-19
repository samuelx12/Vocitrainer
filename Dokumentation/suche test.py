# Suchbegriff
search_prompt = "Gelb Haus Berlin"

# Wörter aus dem Suchbegriff extrahieren
words = search_prompt.split()


results = ['asdfsdf asdf in Befdrlin', 'Reise nach Berlin', "Gelbe Hauser", "Haus Berlin Gelb", "Berliner Küche"]

# Funktion zum Zählen der übereinstimmenden Wörter


def zaehle_treffer(title: str) -> int:
    """
    Zählt die Anzahl Wörter im Titel, die im Suchbegriff vorkommen.
    :param title: Der Titel in dem gesucht werden soll
    :return: Die Anzahl der Wörter im Titel, die im Suchbegriff vorkommen.
    """
    anz_treffer = sum(wort.lower() in title.lower() for wort in words)
    return anz_treffer


# Ergebnisse sortieren
results.sort(key=lambda result: zaehle_treffer(result), reverse=True)

print(results)




import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('../Client/books.db')
c = conn.cursor()

# Suchbegriff
search_prompt = "Gelb Haus Berlin"

# Wörter aus dem Suchbegriff extrahieren
words = search_prompt.split()

# SQL-Abfrage erstellen
query = "SELECT * FROM books WHERE "
for word in words:
    query += f"title LIKE '%{word}%' OR "

# Letztes 'OR' entfernen
query = query[:-3]

# Abfrage ausführen
c.execute(query)

# Ergebnisse abrufen
results = c.fetchall()

# Funktion zum Zählen der übereinstimmenden Wörter
def count_matches(title):
    return sum(word.lower() in title.lower() for word in words)

# Ergebnisse sortieren
results.sort(key=lambda result: count_matches(result[0]), reverse=True)

# Ergebnisse ausgeben
for result in results:
    print(result)