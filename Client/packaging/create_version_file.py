# -*- coding: utf-8 -*-
"""
create_version_file.py
Versionsinfo für Pyinstaller erstellen
"""

import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="0.2.0",
    company_name="admuel",
    file_description="Vocitrainer",
    internal_name="vocitrainer",
    original_filename="vocitrainer.exe",
    product_name="Vocitrainer",
    translations=[1031]
)
