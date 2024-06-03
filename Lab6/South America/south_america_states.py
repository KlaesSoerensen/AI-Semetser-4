from enum import Enum, auto


class States(Enum):
    Colombia = auto()
    Venezuela = auto()
    Guyana = auto()
    Suriname = auto()
    Guyane_Fr = auto()
    Ecuador = auto()
    Peru = auto()
    Brasil = auto()
    Bolivia = auto()
    Paraguay = auto()
    Chile = auto()
    Argentina = auto()
    Uruguay = auto()

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.name)