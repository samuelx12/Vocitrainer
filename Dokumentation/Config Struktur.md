# Dokumentation der Config
***
## Funktionsweise von configobj
```python
from configobj import ConfigObj

# Erstellen einer Konfigurationsdatei
config = ConfigObj()

# Hinzufügen von Abschnitten und Schlüssel-Wert-Paaren
config['Section1'] = {'Key1': 'Wert1', 'Key2': 'Wert2'}
config['Section2'] = {'Key3': 'Wert3', 'Key4': 'Wert4'}

# Schreiben der Konfigurationsdatei
config.write('config.ini')

# Lesen von Konfigurationsdateien
config = ConfigObj('config.ini')

# Zugriff auf Werte
value1 = config['Section1']['Key1']
value3 = config['Section2']['Key3']

# Ändern von Werten
config['Section1']['Key2'] = 'NeuerWert'
config.write()

# Kommentare hinzufügen
config.comments['Section1'] = {'Key1': 'Dies ist ein Kommentar für Key1'}
config.write()
```
***
## Struktur

- Profil
  - email
  - passwort
  - nickname
  - eingeloggt
