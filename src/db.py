import os
from dotenv import set_key
import sqlite3 as sqlite

from copy import deepcopy
from typing import Final

from dotenv import load_dotenv


class Table:
    def __init__(self, name: str, dict_columns: dict[str, list[str]]):
        self._name: Final[str] = name
        self._dict_columns: dict[str, list[str]] = dict_columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> dict[str, list[str]]:
        return deepcopy(self._dict_columns)

    @property
    def columns_name(self):
        return self._dict_columns.keys()

    @property
    def columns_types(self):
        return self._dict_columns.values()

    def str_columns(self) -> str:
        """
        return a (name1 type1, name2 type2, etc.) string
        """
        to_ret = "("
        separator = ", "
        for (name, elem_type) in self._dict_columns:
            to_ret += f"{name} {elem_type}{separator}"

        return to_ret[:len(to_ret) - len(separator)] + ")"

    def get_columns_name(self) -> list[str]:
        """
        return (name1, name2, etc.) tuple
        """
        return [e for (e, _) in self._dict_columns]


class SqlDatabase:
    def __init__(self, bool_create: bool, file_name: str):
        self._tables: set[Table] = set()
        self._database: sqlite.Connection
        self._cursor = None

        # types
        load_dotenv()
        self._text_type: Final[str]         = os.getenv("DB_STR_TYPE")
        self._int_type: Final[str]          = os.getenv("DB_INT_TYPE")
        self._float_type: Final[str]        = os.getenv("DB_FLOAT_TYPE")
        self._primary_key_type: Final[str]  = os.getenv("DB_PRIMARY_KEY_TYPE")
        self._unique_type: Final[str]       = os.getenv("DB_UNIQUE_TYPE")
        self._not_null_type: Final[str]     = os.getenv("DB_NOT_NULL_TYPE")
        self._bool_type: Final[str]         = os.getenv("DB_BOOL_TYPE")
        self._foreign_key: Final[str]       = os.getenv("DB_FOREIGN_KEY")
        self._references: Final[str]        = os.getenv("DB_REFERENCES")

        self._connect(file_name)
        
        if bool_create:
            self._create(file_name)
            set_key(".env", "DB_CREATE", 'False')
        

    def _execute(self, query: str):
        print(f"new query: '{query}'")
        self._cursor.execute(query)
        self._commit()

    def _create_link_table(self, table: Table, var_to_link: str):
        """
            create a table that has links with the tables in link

            link: (field_to_link, {table_name1, table_name2, etc.})
        """
        separator: Final[str] = ', '
        to_link = self._create_table(table, False)

        # link primary key
        substring_set: set[str] = {x for x in table.columns_name if var_to_link in x}
        keys_linked: str = f"({separator.join(substring_set)})"  # id -> (user_id, to_watch_id)
        to_link += f'{self._primary_key_type} {keys_linked},'

        # add foreigns
        for name in substring_set:
            stripped = name[: len(name) - len(var_to_link) - 1]
            to_link += f"{self._foreign_key} ({name}) {self._references} {stripped}({var_to_link}),"

        to_link = to_link[:len(to_link)-(len(separator)-1)] + ');'

        print(to_link)
        self._execute(to_link)
        return

    def _create_table(self, table: Table, commit: bool = True) -> str | None:
        separator = ', '
        to_create: str = f'CREATE TABLE IF NOT EXISTS {table.name} ('
        for k in table.columns.keys():
            to_create += f'{k} '
            for e in table.columns[k]:
                to_create += f'{e} '

            to_create += separator  # lower index by 1 to remove last ','

        
        if commit:
            to_create = to_create[:len(to_create) - len(separator)] + ');'
            print(to_create)
            self._execute(to_create)
            return

        return to_create

    def _create(self, file_name: str):

        """
        !!
        for the ids, always use only 'id' for alone table and 'table_name + _id' for foreign keys
        !!        
        """

        table_user: Table = Table('user',
                                  {
                                      'id': [self._text_type, self._primary_key_type, self._not_null_type],
                                      'username': [self._text_type, self._not_null_type]
                                  })

        table_to_watch: Table = Table('to_watch',
                                      {
                                          'id': [self._text_type, self._primary_key_type, self._not_null_type],
                                          'title': [self._text_type, self._unique_type, self._not_null_type],
                                          'description': [self._text_type, self._not_null_type]
                                      })

        table_link: Table = Table('watch_user',
                                  {
                                      'user_id': [self._text_type, self._not_null_type],
                                      'to_watch_id': [self._text_type, self._not_null_type],
                                      'watched': [self._bool_type, self._not_null_type],
                                  })

        table_review: Table = Table('review',
                                    {
                                        'user_id': [self._text_type, self._not_null_type],
                                        'to_watch_id': [self._text_type, self._not_null_type],
                                        'rating': [self._float_type, self._not_null_type],
                                        'spoil_review': [self._text_type],
                                        'non_spoil_review': [self._text_type]
                                    })

        self._tables.add(table_user)
        self._tables.add(table_to_watch)
        self._tables.add(table_link)
        self._tables.add(table_review)
        self._create_table(table_user)
        self._create_table(table_to_watch)
        self._create_link_table(table_link, 'id')
        self._create_link_table(table_review, 'id')

        '''
            look to link keys
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
            PRIMARY KEY (user_id, movie_id)

        '''

    def _connect(self, file_name: str):
        try:
            self._database = sqlite.connect(file_name)
        except:
            raise ConnectionError(f"Can't connect to the given database {file_name}")

        self._cursor = self._database.cursor()


    def _clean(self):
        pass

    def _commit(self):
        try:
            self._database.commit()
        except:
            raise ConnectionError("Could not commit to the database")
