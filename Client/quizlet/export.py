# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from contextlib import suppress
from rich import print as rprint


class QuizletExportFehler(Exception):
    """
    Diese Exceptin wird geworfen, wenn wegen fehlendem Internet keine Karten von Quizlet geladen werden können.
    """
    def __init__(self):
        super().__init__()


def get_quizlet_set(link: str) -> tuple:
    """
    Versucht mit Selenium das Quizlet-Set unter dem angegebenen Link zu exportieren.
    :param link: Link zum Quizletset
    :return: titel, set_daten
    """
    set_liste = []

    firefox_options = Options()
    firefox_options.headless = True
    try:
        browser = webdriver.Firefox(options=firefox_options)
    except:
        raise QuizletExportFehler

    try:

        browser.get(link)

        # Titel laden
        oberer_bereich = browser.find_element(By.ID, "setPageSetIntroWrapper")
        # titel_element = browser.find_element(By.CLASS_NAME, "SetPage-setTitle")
        titel = oberer_bereich.find_element(By.TAG_NAME, "h1").text

        # Set laden
        liste = browser.find_element(By.CLASS_NAME, "SetPageTerms-termsList")

        karten = liste.find_elements(By.CLASS_NAME, "SetPageTerms-term")

        for karte in karten:
            begriffe = karte.find_elements(By.TAG_NAME, "span")
            karte_liste = []
            try:
                karte_liste.append(begriffe[0].text)
            except:
                karte_liste.append("")

            try:
                karte_liste.append(begriffe[1].text)
            except:
                karte_liste.append("")

            set_liste.append(karte_liste)
    except:
        browser.quit()
        raise QuizletExportFehler

    browser.quit()

    return titel, set_liste


if __name__ == "__main__":
    quizlet = "https://quizlet.com/ch/756691941/industries-flash-cards/?funnelUUID=bb7c3c06-52ec-417b-9297-1ea17949e442"
    quizlet2 = "https://quizlet.com/784248493/54-politics-and-public-institutions-flash-cards/?funnelUUID=2045bcc1-bd4f-4c46-b7c4-86a92aceb799"
    ergebnis = get_quizlet_set(quizlet2)
    rprint(ergebnis)
