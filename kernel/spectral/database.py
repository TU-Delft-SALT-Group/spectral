"""Handles all the interactions with the Postgres database."""

from __future__ import annotations

from typing import Self

import psycopg


class Database:
    """
    Database class for interacting with a PostgreSQL database.

    This class handles connecting to the database, fetching files, and closing the connection.

    Attributes
    ----------
        conn (psycopg.Connection): The connection object to the database.
        cursor (psycopg.Cursor): The cursor object to execute database queries.

    Methods
    -------
        fetch_file(id: int) -> dict:
            Fetches a file record from the database by its ID.
        close():
            Closes the database connection and cursor.

    """

    user: str
    password: str
    host: str
    port: str
    dbname: str

    def __init__(self, user: str, password: str, host: str, port: str, dbname: str):  # noqa: PLR0913
        """
        Initialize the Database object and opens a connection to the specified
        PostgreSQL database.

        Args:
        ----
            user (str): The username for the database.
            password (str): The password for the database.
            host (str): The host address of the database.
            port (str): The port number for the database.
            dbname (str): The name of the database.

        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

    def connection(self: Self) -> None:
        """Establish the connection the database and setup cursor."""
        self.conn = psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cursor = self.conn.cursor()

    def fetch_apikey(self: Self, user_id: str, model_name: str) -> str | None:
        """
        Fetch an api key for a certain model from a particular user.

        Args:
        ----
            user_id (str): the id of the user.
            model_name (str): the name of the model for which api key is requested.

        Returns:
        -------
            str | None: either an api key or None

        """
        self.cursor.execute("""
            SELECT column_name, ordinal_position
            FROM information_schema.columns
            WHERE table_name = 'user'
        """)
        column_data = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM user WHERE id = %s", [user_id])
        db_res = self.cursor.fetchone()  # type: ignore

        print("!!!!!!!!!!!!!")
        print(db_res)
        return None

    def fetch_file(self: Self, file_id: str) -> dict:
        """
        Fetch a file record from the database by its ID.

        Args:
        ----
            file_id (str): The ID of the file to fetch.

        Returns:
        -------
            dict: A dictionary containing the file record's details.

        """
        self.cursor.execute("""
            SELECT column_name, ordinal_position
            FROM information_schema.columns
            WHERE table_name = 'files'
        """)
        column_data = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM files WHERE id = %s", [file_id])
        db_res = self.cursor.fetchone()  # type: ignore

        if db_res is None:
            raise FileNotFoundError

        result = {}
        for column in column_data:
            result[self.snake_to_camel(column[0])] = db_res[column[1] - 1]
        return result

    def snake_to_camel(self, snake_case_str: str) -> str:
        """
        Convert a snake_case string to camelCase.

        Parameters
        ----------
        - snake_case_str (str): The snake_case string to be converted.

        Returns
        -------
        - str: The camelCase version of the input string.

        Example:
        ```python
        camel_case_str = self.snake_to_camel('example_string')
        ```

        """
        components = snake_case_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def get_transcriptions(self, file_id: str) -> list[list]:
        """
        Fetch transcriptions associated with a file from the database.

        Args:
        ----
            file_id (str): The ID of the file to fetch transcriptions for.

        Returns:
        -------
            list: A list of lists containing transcription entries,
                  where each inner list represents a file transcription
                  and contains dictionaries with "start", "end", and "value" keys.

        """
        self.cursor.execute(
            """
                           SELECT id FROM file_transcription
                           WHERE file = %s
                           """,
            [file_id],
        )
        file_transcriptions = self.cursor.fetchall()
        res = []
        for file_transcription in file_transcriptions:
            self.cursor.execute(
                """
                           SELECT start, "end", value FROM transcription
                           WHERE file_transcription = %s
                           """,
                [file_transcription[0]],
            )
            transcriptions = self.cursor.fetchall()
            parsed_file_transcriptions = [
                {
                    "start": transcription[0],
                    "end": transcription[1],
                    "value": transcription[2],
                }
                for transcription in transcriptions
            ]
            res.append(parsed_file_transcriptions)
        return res

    def close(self) -> None:
        """Close the database connection and cursor."""
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except NameError:
            pass
