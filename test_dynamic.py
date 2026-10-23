from typing import Optional
from datetime import date

class Pruefungsleistung:
    def __init__(self, note: Optional[float] = None, abschlussdatum: Optional[date] = None):
        self._note = note
        self._abschlussdatum = abschlussdatum

    @property
    def ist_bestanden(self) -> bool:
        if self._note is None:
            return False
        return self._note <= 4.0
    