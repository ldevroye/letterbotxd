from typing import Final

from src.db import SqlDatabase
from src.common import RequestType, to_watch, rate, print_err


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

    def get_user(self, user_id: str):
        raise NotImplementedError

    def get_to_watch(self, to_watch_id: str):
        raise NotImplementedError

    def get_review(self, user_id: str, to_watch_id: str):
        raise NotImplementedError

    def get_rating(self, to_watch_id: str, user_id):
        raise NotImplementedError

    def get_user_to_watch(self, user_id: str):
        raise NotImplementedError

    def get_to_watch_users(self, to_watch_id: str):
        raise NotImplementedError

    def get_ratings_to_watch(self, to_watch_id: str):
        raise NotImplementedError

    def get_user_ratings(self, user_id: str):
        raise NotImplementedError

    def add_user(self, user_id: str, user_name: str):
        raise NotImplementedError

    def add_to_watch(self, to_watch_id: str, to_watch_title: str, to_watch_desc: str = None):
        raise NotImplementedError

    def add_review(self, to_watch_id: str, user_id: str,
                   spoil_review: str = None, non_spoil_review: str = None, rating: rate = None):
        raise NotImplementedError

    def change_review(self, to_watch_id: str, user_id: str,
                      spoil_review: str = None, non_spoil_review: str = None, rating: rate = None):
        raise NotImplementedError

    def remove_to_watch(self, to_watch_id: str):
        raise NotImplementedError

    def remove_review(self, to_watch_id: str, user_id: str):
        raise NotImplementedError

    def remove_user(self, user_id: str):
        raise NotImplementedError

    def pick_movie(self, user_id: str):
        raise NotImplementedError

    def interact_db(self, request_type: RequestType, **options):
        """
        Private fn to make request to the db
        """
        str_user_id: Final[str] = 'user_id'
        str_user_name: Final[str] = 'user_name'

        str_to_watch_id: Final[str] = 'to_watch_id'
        str_to_watch_title: Final[str] = 'to_watch_title'

        str_spoil_review: Final[str] = 'spoil_review'
        str_non_spoil_review: Final[str] = 'non_spoil_review'
        str_rating: Final[str] = 'rating'

        user_id: str = None
        user_name: str = None

        to_watch_id: str = None
        to_watch_title: str = None

        spoil_review: str = None
        non_spoil_review: str = None
        rating: rate = None

        lst_unknown: list[str] = []
        for k in options.keys():
            if k == str_user_id:
                user_id = options[str_user_id]
            if k == str_user_name:
                user_name = options[str_user_name]

            elif k == str_to_watch_id:
                to_watch_id = options[str_user_id]
            elif k == str_to_watch_title:
                to_watch_title = options[str_to_watch_title]

            elif k == str_spoil_review:
                spoil_review = options[str_spoil_review]
            elif k == str_non_spoil_review:
                non_spoil_review = options[str_non_spoil_review]
            elif k == rating:
                rating = options[str_rating]

            else:
                lst_unknown.append(k)

        if len(lst_unknown) > 0:
            print_err(f"Unknown keys: {lst_unknown}")

        # POV: you're piratesoftware
        lst_needed: list[str] = []
        match request_type:
            case RequestType.GET_USER:  # (user_id: user_infos)
                if user_id is not None:
                    self.get_user(user_id)
                    return
                lst_needed.append(str_user_id)

            case RequestType.GET_TO_WATCH:  # (to_watch_id: to_watch_infos)
                if to_watch_id is not None:
                    self.get_to_watch(to_watch_id)
                    return
                lst_needed.append(str_to_watch_id)

            case RequestType.GET_REVIEW:  # ((to_watch_id, user_id): review)
                if to_watch_id is not None and user_id is not None:
                    self.get_review(to_watch_id=to_watch_id, user_id=user_id)
                    return
                lst_needed.extend([str_user_id, str_to_watch_id])

            case RequestType.GET_RATING:  # ((to_watch_id, user_id): rating)
                if to_watch_id is not None and user_id is not None:
                    self.get_rating(to_watch_id=to_watch_id, user_id=user_id)
                    return
                lst_needed.extend([str_user_id, str_to_watch_id])

            case RequestType.GET_LIST_USER_TO_WATCH:  # (user_id: list_to_watch)
                if user_id is not None:
                    self.get_user_to_watch(user_id)
                    return
                lst_needed.append(str_user_id)

            case RequestType.GET_LIST_TO_WATCH_USERS:  # (to_watch_id: list_user)
                if to_watch_id is not None:
                    self.get_to_watch_users(to_watch_id)
                    return
                lst_needed.append(str_to_watch_id)

            case RequestType.GET_RATINGS_TO_WATCH:  # (to_watch_id: list_ratings)
                if to_watch_id is not None:
                    self.get_ratings_to_watch(to_watch_id)
                    return
                lst_needed.append(str_to_watch_id)

            case RequestType.GET_USER_RATINGS:  # (user_id: list_ratings)
                if user_id is not None:
                    self.get_user_ratings(user_id)
                    return
                lst_needed.append(str_user_id)

            case RequestType.ADD_USER:
                if user_id and user_name:
                    self.add_user(user_id=user_id, user_name=user_name)

                lst_needed.extend([str_user_id, str_user_name])

            case RequestType.ADD_REVIEW:
                if user_id and to_watch_id and (non_spoil_review or spoil_review or rating):
                    self.add_review(user_id=user_id,
                                    to_watch_id=to_watch_id,
                                    non_spoil_review=non_spoil_review,
                                    spoil_review=spoil_review,
                                    rating=rating)

                lst_needed.extend([str_user_id, str_user_name, str_spoil_review, str_non_spoil_review, str_rating])

            case RequestType.ADD_TO_WATCH:
                if to_watch_id and to_watch_title:
                    self.add_to_watch(to_watch_id=to_watch_id, to_watch_title=to_watch_title)

            case RequestType.CHANGE_REVIEW:
                if user_id and to_watch_id and (non_spoil_review or spoil_review or rating):
                    self.change_review(user_id=user_id,
                                       to_watch_id=to_watch_id,
                                       non_spoil_review=non_spoil_review,
                                       spoil_review=spoil_review,
                                       rating=rating)
                lst_needed.extend([str_user_id, str_user_name, str_spoil_review, str_non_spoil_review, str_rating])

            case RequestType.REMOVE_TO_WATCH:
                if to_watch_id:
                    self.remove_to_watch(to_watch_id)

                lst_needed.append(to_watch_id)

            case RequestType.REMOVE_REVIEW:
                if to_watch_id and user_id:
                    self.remove_review(to_watch_id=to_watch_id, user_id=user_id)

                lst_needed.extend([to_watch_id, user_id])

            case RequestType.REMOVE_USER:
                if user_id:
                    self.remove_user(user_id)

                lst_needed.extend(user_id)

            case RequestType.PICK_MOVIE:
                if user_id:
                    self.pick_movie(user_id)

                lst_needed.append(user_id)

            case _:
                raise NotImplementedError(
                    f"Request type ({request_type.name} : {request_type.value}) not yet implemented")

        raise ValueError(
            f"Wrong arguments for {request_type.name}:"
            f" {options.keys()} where passed when {lst_needed} was needed.")
