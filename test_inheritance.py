class NotenZiel(Ziel):
    def __init__(self, bezeichnung: str, ziel_notendurchschnitt: float):
        super().__init__(bezeichnung)
        self._ziel_notendurchschnitt = ziel_notendurchschnitt

    def berechne_fortschritt(self) -> float:
        # Logik zum Abgleich des Ist-Durchschnitts mit dem Zielwert, aktuell durch folgenden Platzhalter ersetzt
        return 0.0
