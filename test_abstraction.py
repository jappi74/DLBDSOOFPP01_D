from abc import ABC, abstractmethod

class Ziel(ABC):
    def __init__(self, bezeichnung: str):
        self._bezeichnung = bezeichnung

    @abstractmethod
    def berechne_fortschritt(self) -> float:
        pass
