# -*- coding: utf-8 -*-
"""
karte_tuple.py
'Karte' ist ein namedtuple für die bessere Lesbarkeit des Codes. In diesem werden die Informationen eines
Kartendatensatzes gespeichert.
Es wird vom Trainingsfenster benutzt.
"""

from collections import namedtuple

Karte = namedtuple(
    "Karte",
    [
        "ID",
        "wort",
        "fremdwort",
        "definition",
        "bemerkung",
        "lernfortschritt",
        "markiert",
        "schwierigkeit_max",
        "schwierigkeit_training"
    ]
)
