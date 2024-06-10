import psycopg


class Database:
    """
    Database class for interacting with a PostgreSQL database.

    This class handles connecting to the database, fetching files, and closing the connection.

    Attributes:
        conn (psycopg.Connection): The connection object to the database.
        cursor (psycopg.Cursor): The cursor object to execute database queries.

    Methods:
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

    def __init__(self, user: str, password: str, host: str, port: str, dbname: str):
        """
        Initializes the Database object and opens a connection to the specified PostgreSQL database.

        Args:
            user (str): The username for the database.
            password (str): The password for the database.
            host (str): The host address of the database.
            port (int): The port number for the database.
            dbname (str): The name of the database.
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

    def connection(self) -> None:
        self.conn = psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cursor = self.conn.cursor()

    def fetch_file(self, id: str) -> dict:
        """
        Fetches a file record from the database by its ID.

        Args:
            id (str): The ID of the file to fetch.

        Returns:
            dict: A dictionary containing the file record's details.
        """
        self.cursor.execute("""
            SELECT column_name, ordinal_position
            FROM information_schema.columns
            WHERE table_name = 'files'
        """)
        column_data = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM files WHERE id = %s", [id])
        db_res = self.cursor.fetchone()  # type: ignore

        if db_res is None:
            raise FileNotFoundError

        result = {}
        for column in column_data:
            result[self.snake_to_camel(column[0])] = db_res[column[1] - 1]
        return result

    def snake_to_camel(self, snake_case_str: str) -> str:
        """
        Converts a snake_case string to camelCase.

        Parameters:
        - snake_case_str (str): The snake_case string to be converted.

        Returns:
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
        Fetches transcriptions associated with a file from the database.

        Args:
            file_id (str): The ID of the file to fetch transcriptions for.

        Returns:
            list: A list of lists containing transcription entries, where each inner list represents a file transcription and contains dictionaries with "start", "end", and "value" keys.
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
            parsed_file_transcriptions = []
            for transcription in transcriptions:
                parsed_file_transcriptions.append(
                    {
                        "start": transcription[0],
                        "end": transcription[1],
                        "value": transcription[2],
                    }
                )
            res.append(parsed_file_transcriptions)
        return res

    def close(self) -> None:
        """
        Closes the database connection and cursor.
        """
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except NameError:
            pass
