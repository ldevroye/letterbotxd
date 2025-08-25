from typing import Final

from src.db import SqlDatabase
from src.common import RequestType, to_watch, rate


class PyDatabase:
    """
    Cache database for the SQL
    """

    def __init__(self, sql_db: SqlDatabase):
        """
        No review in the cache as they are too long and not requested often.
        """
        self._lst_movie: list[to_watch] = list()

        # {movie: {user: rating}}
        self._lst_ratings: dict[id: dict[id: rate]] = dict()

        self._db: SqlDatabase = sql_db

    def get_average_rating(self, m_id: id) -> rate:
        if self._lst_ratings is None:
            raise RuntimeError("Error in the ratings dictionary (None)")

        rates: dict[id: rate] = self._lst_ratings.get(m_id)

        if rates is None or len(rates) < 1:
            raise KeyError("This movie/anim doesn't exists in the list")

        return sum(rates.values) / len(rates)

    def _db_get_user(self, user_id: str):
        raise NotImplementedError

    def _db_get_to_watch(self, to_watch_id: str):
        raise NotImplementedError

    def _db_get_review(self, user_id: str, to_watch_id: str):
        raise NotImplementedError

    def _db_get_rating(self, to_watch_id: str, user_id):
        raise NotImplementedError

    def _db_get_user_to_watch(self, user_id: str):
        raise NotImplementedError

    def _db_get_to_watch_users(self, to_watch_id: str):
        raise NotImplementedError

    def _db_get_ratings_to_watch(self, to_watch_id: str):
        raise NotImplementedError

    def _db_get_user_ratings(self, user_id: str):
        raise NotImplementedError

    def interact_db(self, request_type: RequestType, **options):
        """
        Private fn to make request to the db
        """
        str_id_user: Final[str] = 'user_id'
        str_id_to_watch: Final[str] = 'to_watch_id'
        user_id: str = None
        to_watch_id: str = None

        for k in options.keys():
            if k == str_id_user:
                user_id = options[str_id_user]

            elif k == str_id_to_watch:
                to_watch_id = options[str_id_user]

            else:
                print(f"Unknown key: {k}")

        # POV: you're piratesoftware
        match request_type:
            case RequestType.GET_USER:  # (user_id: user_infos)
                if user_id is not None:
                    self._db_get_user(user_id)
                    return

            case RequestType.GET_TO_WATCH:  # (to_watch_id: to_watch_infos)
                if to_watch_id is not None:
                    self._db_get_to_watch(to_watch_id)
                    return

            case RequestType.GET_REVIEW:  # ((to_watch_id, user_id): review)
                if to_watch_id is not None and user_id is not None:
                    self._db_get_review(to_watch_id=to_watch_id, user_id=user_id)
                    return

            case RequestType.GET_RATING:  # ((to_watch_id, user_id): rating)
                if to_watch_id is not None and user_id is not None:
                    self._db_get_rating(to_watch_id=to_watch_id, user_id=user_id)
                    return

            case RequestType.GET_LIST_USER_TO_WATCH:  # (user_id: list_to_watch)
                if user_id is not None:
                    self._db_get_user_to_watch(user_id)
                    return

            case RequestType.GET_LIST_TO_WATCH_USERS:  # (to_watch_id: list_user)
                if to_watch_id is not None:
                    self._db_get_to_watch_users(to_watch_id)
                    return

            case RequestType.GET_RATINGS_TO_WATCH:  # (to_watch_id: list_ratings)
                if to_watch_id is not None:
                    self._db_get_ratings_to_watch(to_watch_id)
                    return

            case RequestType.GET_USER_RATINGS:  # (user_id: list_ratings)
                if user_id is not None:
                    self._db_get_user_ratings(user_id)
                    return

            case _:
                raise NotImplementedError(
                    f"Request type ({request_type.name} : {request_type.value}) not yet implemented")

        list_not_none = [(e, options[e]) for e in options.keys()]
        raise RuntimeError(f"{request_type.name}, ({list_not_none[0]}: {list_not_none[1]}) are not None")

