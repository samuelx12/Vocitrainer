from whoosh.index import create_in
from whoosh.fields import TEXT, Schema

# Erstelle ein Schema, das die Felder in deinem Dokument definiert
schema = Schema(title=TEXT(stored=True), content=TEXT)

# Erstelle einen Index
index = create_in("my_index", schema)

# Öffne den Index für Schreibzugriff
writer = index.writer()

# Füge Dokumente zum Index hinzu
writer.add_document(title="Dokument 1", content="Dies ist der Inhalt des ersten Dokuments.")
writer.add_document(title="Dokument 2", content="Das zweite Dokument enthält weitere Informationen.")

# Beende das Schreiben und speichere den Index
writer.commit()

# Durchsuche den Index
from whoosh.qparser import QueryParser

# Erstelle einen Parser für Suchanfragen
parser = QueryParser("content", schema=schema)

# Erstelle eine Suchanfrage
query = parser.parse("Dokument 4")

# Suche im Index
from whoosh.searching import Searcher

with index.searcher() as searcher:
    results = searcher.search(query)
    for result in results:
        print(result)