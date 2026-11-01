import json
from pathlib import Path
from datetime import date
from models import Student, Studiengang, Modul, Pruefungsleistung, PruefungsForm, NotenZiel, ZeitZiel

class JsonRepository:
    def __init__(self, dateipfad: str = "studien_daten.json"):
        self._dateipfad = Path(dateipfad)

    def lade_daten(self) -> Student:
        # Erzeugen einer JSON Datei, falls sie nicht existiert
        if not self._dateipfad.exists():
            self._erstelle_default_json()

        # JSON-Datei einlesen
        with open(self._dateipfad, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Deserialisierung der Module
        studiengang_data = data["studiengang"]
        module = []
        for m in studiengang_data["module"]:
            pl_data = m["pruefungsleistung"]
            
            # Enum-Mapping der Prüfungsformen
            form_enum = PruefungsForm(pl_data["pruefungsform"])
            
            pl = Pruefungsleistung(
                pruefungsform=form_enum,
                note=pl_data["note"],
                abschlussdatum=date.fromisoformat(pl_data["abschlussdatum"]) if pl_data["abschlussdatum"] else None
            )
            module.append(Modul(m["bezeichnung"], m["credit_points"], pl))

        studiengang = Studiengang(
            name=studiengang_data["name"],
            startdatum=date.fromisoformat(studiengang_data["startdatum"]),
            regelstudienzeit=studiengang_data["regelstudienzeit"],
            credit_points_total=studiengang_data["credit_points_total"],
            module=module
        )

        # Deserialisierung der JSON-Studiendaten
        ziele = []
        for z in data["ziele"]:
            if "ziel_notendurchschnitt" in z and z["ziel_notendurchschnitt"] is not None:
                ziele.append(NotenZiel(z["bezeichnung"], z["ziel_notendurchschnitt"]))
            elif "geplantes_enddatum" in z and z["geplantes_enddatum"] is not None:
                ziele.append(ZeitZiel(z["bezeichnung"], date.fromisoformat(z["geplantes_enddatum"])))

        return Student(name=data["name"], studiengang=studiengang, ziele=ziele)

    def _erstelle_default_json(self) -> None:
        # Hilfsweises Initialisieren der Studiendaten JSON-Datei, falls nicht vorhanden
        default_data = {
            "name": "Max Mustermann",
            "studiengang": {
                "name": "Bachelor of Science - Cybersecurity",
                "startdatum": "2025-05-01",
                "regelstudienzeit": 3,
                "credit_points_total": 180,
                "module": [
                    {
                        "bezeichnung": "Platzhaltermodul",
                        "credit_points": 5,
                        "pruefungsleistung": {
                            "pruefungsform": "Klausur",
                            "note": 1.3,
                            "abschlussdatum": "2025-08-15"
                        }
                    }
                ]
            },
            "ziele": [
                {
                    "bezeichnung": "Notendurchschnitt anstreben",
                    "ziel_notendurchschnitt": 2.0
                }
            ]
        }
        with open(self._dateipfad, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)