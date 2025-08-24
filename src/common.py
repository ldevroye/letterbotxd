import uuid
from dataclasses import dataclass
from typing import Final, Iterable


@dataclass(frozen=True)
class rate:
    value: float

    def __post_init__(self):
        if not (-1 <= self.value <= 5):
            raise ValueError("Rate must be between -1 and 5.")


uninitialised_rate: rate = rate(-1.0)


@dataclass
class to_watch:
    """
    Abrstact class for Movie, Season and Series as they are independents, but they are the same conceptual object
    """

    def __init__(self, name: str, desc: str, types: set[str] = None):
        self._id: Final[uuid] = uuid.UUID(name)
        self._name: Final[str] = name
        self._desc: Final[str] = desc
        self._rating: rate = uninitialised_rate  # initialised at -1 should be [0;5]

        if types is None:
            types = set()
        self._types: set[str] = types

    @property
    def id(self) -> uuid:
        return self._id

    @property
    def id_int(self) -> int:
        return self._id.int

    @property
    def name(self) -> str:
        return self.name

    @property
    def desc(self) -> str:
        return self.desc

    def has_type(self, type_searched: str):
        if type_searched in self._types:
            return True

        return False

    def has_types(self, types_searched: set[str]):
        if len(types_searched) > len(self._types):
            return False

        for elem in types_searched:
            if elem not in self._types:
                return False

        return True

    def add_types(self, to_add: Iterable[str]):
        for elem in to_add:
            self._types.add(elem)

    def add_type(self, to_add: str):
        self._types.add(to_add)
