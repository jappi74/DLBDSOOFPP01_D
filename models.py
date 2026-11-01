from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List
from datetime import date

class PruefungsForm(Enum):
    KLAUSUR = "Klausur"
    HAUSARBEIT = "Hausarbeit"
    PROJEKTARBEIT = "Projektarbeit"
    PRAESENTATION = "Präsentation"

# Hilfsklasse ABC definieren um abstrakte Basisklassen(Ziele) modellieren zu können
class Ziel(ABC):
    def __init__(self, bezeichnung: str):
        self._bezeichnung = bezeichnung

    @property
    def bezeichnung(self) -> str:
        return self._bezeichnung

    @abstractmethod
    def berechne_fortschritt(self) -> float:
        pass

class NotenZiel(Ziel):
    def __init__(self, bezeichnung: str, ziel_notendurchschnitt: float):
        super().__init__(bezeichnung)
        self._ziel_notendurchschnitt = ziel_notendurchschnitt

    @property
    def ziel_notendurchschnitt(self) -> float:
        return self._ziel_notendurchschnitt

    def berechne_fortschritt(self) -> float:
        return self._ziel_notendurchschnitt

class ZeitZiel(Ziel):
    def __init__(self, bezeichnung: str, geplantes_enddatum: date):
        super().__init__(bezeichnung)
        self._geplantes_enddatum = geplantes_enddatum

    @property
    def geplantes_enddatum(self) -> date:
        return self._geplantes_enddatum

    def berechne_fortschritt(self) -> float:
        return 100.0

class Pruefungsleistung:
    def __init__(self, pruefungsform: PruefungsForm, note: Optional[float] = None, abschlussdatum: Optional[date] = None):
        self._pruefungsform = pruefungsform
        self._note = note
        self._abschlussdatum = abschlussdatum

    @property
    def pruefungsform(self) -> PruefungsForm:
        return self._pruefungsform

    @property
    def note(self) -> Optional[float]:
        return self._note

    @property
    def abschlussdatum(self) -> Optional[date]:
        return self._abschlussdatum

    @property
    def ist_bestanden(self) -> bool:
        if self._note is None:
            return False
        return self._note <= 4.0

class Modul:
    def __init__(self, bezeichnung: str, credit_points: int, pruefungsleistung: Pruefungsleistung):
        self._bezeichnung = bezeichnung
        self._credit_points = credit_points
        self._pruefungsleistung = pruefungsleistung

    @property
    def bezeichnung(self) -> str:
        return self._bezeichnung

    @property
    def credit_points(self) -> int:
        return self._credit_points

    @property
    def pruefungsleistung(self) -> Pruefungsleistung:
        return self._pruefungsleistung

class Studiengang:
    def __init__(self, name: str, startdatum: date, regelstudienzeit: int, credit_points_total: int, module: List[Modul] = None):
        self._name = name
        self._startdatum = startdatum
        self._regelstudienzeit = regelstudienzeit
        self._credit_points_total = credit_points_total
        self._module = module if module is not None else []

    @property
    def name(self) -> str:
        return self._name

    @property
    def startdatum(self) -> date:
        return self._startdatum

    @property
    def regelstudienzeit(self) -> int:
        return self._regelstudienzeit

    @property
    def credit_points_total(self) -> int:
        return self._credit_points_total

    @property
    def module(self) -> List[Modul]:
        return self._module

    def berechne_ects_fortschritt(self) -> int:
        return sum(m.credit_points for m in self._module if m.pruefungsleistung.ist_bestanden)

class Student:
    def __init__(self, name: str, studiengang: Studiengang, ziele: List[Ziel] = None):
        self._name = name
        self._studiengang = studiengang
        self._ziele = ziele if ziele is not None else []

    @property
    def name(self) -> str:
        return self._name

    @property
    def studiengang(self) -> Studiengang:
        return self._studiengang

    @property
    def ziele(self) -> List[Ziel]:
        return self._ziele