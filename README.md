# DLBDSOOFPP01_D

Installationsanleitung: Studiendashboard

Im Folgenden wird die Installation und Verwendung des Programmcodes aus dem Projekt dargestellt. Getestet wurde Alles auf Windows 11 mit Python 3.12.10 und dem Web-Browser Firefox in der Version 157.0.

Installation

Bitte verwenden Sie ein aktuelles Windows-Betriebssystem wie Windows 11 mit installiertem Web-Browser. Installieren Sie dann zunächst die Python Version 3.12 inklusive des Paketmanagers pip https://www.python.org/downloads/latest/python3.12/ .


Klonen Sie das Repository mit folgendem Befehl:
git clone https://github.com/jappi74/DLBDSOOFPP01_D.git

Wechseln Sie anschließend auf der CLI in den Projektordner und installieren Sie die Abhängigkeiten. Das Projekt verwendet neben der Python-Standardbibliothek weitere externe Bibliotheken, die manuell installiert werden müssen:
pip install streamlit plotly

Verwendung

Zum Starten des Dashboards führen Sie die Datei main.py wie folgt aus:
streamlit run main.py

Zum Beenden des Programmes schließen Sie den Browsertab und brechen den Prozess auf der CLI mit der Tastenkombination STRG+C ab.

Sollten Sie andere Daten als die vordefinierten Studiendaten in studien_daten.json testen wollen, muss die JSON-Datei entsprechend angepasst und das Dashboard neu gestartet werden.




