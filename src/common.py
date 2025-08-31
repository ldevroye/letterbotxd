import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Final, Iterable

_bgn_print_red: Final[str] = "\033[91m"
_end_print_red: Final[str] = "\033[0m"


def print_err(err: str):
    """
    Prints '[ERROR] {err}' in red
    """
    print(f"{_bgn_print_red}[ERROR] {err}{_end_print_red}")


class RequestType(Enum):
    GET_USER = 0  # (id_user: user_infos)
    GET_TO_WATCH = 1  # (id_to_watch: to_watch_infos)
    GET_REVIEW = 2  # ((id_to_watch, id_user): review)
    GET_RATING = 3  # ((id_to_watch, id_user): rating)
    GET_LIST_USER_TO_WATCH = 4  # (id_user: list_to_watch)
    GET_LIST_TO_WATCH_USERS = 5  # (id_to_watch: list_user)
    GET_RATINGS_TO_WATCH = 6  # (id_to_watch: list_ratings)
    GET_USER_RATINGS = 7  # (id_user: list_ratings)

    ADD_USER = 8  # (id_user, name)
    ADD_TO_WATCH = 9  # (id_to_watch, title, description)
    ADD_REVIEW = 10  # (user_id, to_watch_id, rating, spoil_review, non_spoil_review)

    CHANGE_REVIEW = 11  # (user_id, to_watch_id, rating, spoil_review, non_spoil_review)

    REMOVE_TO_WATCH = 12  # (id_to_watch)
    REMOVE_REVIEW = 13  # (id_to_watch, id_user)
    REMOVE_USER = 14  # (id_user)

    PICK_MOVIE = 15  # (id_user)

    _NOT_IMPLEMENTED = 999



@dataclass(frozen=True)
class rate:
    value: float

    def __post_init__(self):
        if not (-1 <= self.value <= 5):
            raise ValueError("Rate must be between -1 and 5.")


uninitialised_rate: Final[rate] = rate(-1.0)


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
