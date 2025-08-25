from src.common import *


class User:
    def __init__(self, name: str, discord_id: str):
        self._name: str = name
        self._discord_id: Final[str] = discord_id
        # set{uuid1, uuid2, uuid3, ..}
        self._lst_to_watch: set[uuid] = set()

        # dict{uuid: (rate, spoil, non_spoil)}
        self._lst_watched: dict[uuid: tuple[rate, str, str]] = dict()

    def update_name(self, new_name: str):
        self._name = new_name

    def add_to_watch(self, to_add: uuid):
        if self._lst_to_watch is None:
            self._lst_to_watch = set()

        self._lst_to_watch.add(to_add)

    def add_watched(self, to_add: uuid, rating: rate, non_spoil_opinion: str = "", spoil_opinion: str = ""):
        if self._lst_to_watch is not None and \
                to_add in self._lst_to_watch:
            self._lst_to_watch.remove(to_add)

        if self._lst_watched is None:
            self._lst_watched = dict()

        self._lst_watched[to_add] = (rating, spoil_opinion, non_spoil_opinion)


class Movie(to_watch):
    def __init__(self, name: str, desc: str, types: Iterable[str] = None):
        super().__init__(name, desc, types)


class Season(to_watch):
    def __init__(self, name: str, desc: str = "", episodes: Iterable[Movie] = None, types: Iterable[str] = None):
        super().__init__(name, desc, types)

        self._episodes: set[Movie]
        if episodes is None:
            self._episodes = set()
        else:
            self._episodes = set(episodes)

    def add_ep(self, to_add: Movie):
        if self._episodes is None:
            self._episodes = set()

        self._episodes.add(to_add)

    def add_mul_ep(self, to_add: set[Movie]):
        if self._episodes is None:
            self._episodes = set(to_add)
            return

        for elem in to_add:
            self._episodes.add(elem)


class Series(to_watch):
    def __init__(self, name: str, desc: str = "", types: Iterable[str] = None):
        super().__init__(name, desc, types)
        self._seasons: set[Season] = set()

    def add_season(self, to_add: Season):
        if self._seasons is None:
            self._seasons = set()

        self._seasons.add(to_add)

