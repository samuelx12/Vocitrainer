# -*- coding: utf-8 -*-
"""
karte_tuple.py
'Karte_alt' ist ein namedtuple für die bessere Lesbarkeit des Codes. In diesem werden die Informationen eines
Kartendatensatzes gespeichert.
Es wird vom Trainingsfenster benutzt.

Eine noch bessere Lösung ist die neue Dataclass Klasse 'Karte', weil sie mutabel ist.
"""

from collections import namedtuple
from dataclasses import dataclass

Karte_alt = namedtuple(
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


@dataclass
class Karte:
    """
    In dieser Klasse werden die Informationen zu einem Wort gespeichert mit allem drum und dran.
    """
    ID: int
    wort: str
    fremdwort: str
    definition: str
    bemerkung: str
    lernfortschritt: int
    markiert: int  # Eigentlich bool, aber das gibt es auch in der DB nicht deshalb int mit 0 oder 1
    schwierigkeit_max: int
    schwierigkeit_training: int = 2
