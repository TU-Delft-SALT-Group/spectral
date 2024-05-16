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
    def __init__(self, user, password, host, port, dbname):
        """
        Initializes the Database object and opens a connection to the specified PostgreSQL database.

        Args:
            user (str): The username for the database.
            password (str): The password for the database.
            host (str): The host address of the database.
            port (int): The port number for the database.
            dbname (str): The name of the database.
        """
        self.conn = psycopg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("database connection opened")
        self.cursor = self.conn.cursor()
    
    def fetch_file(self,id):
        """
        Fetches a file record from the database by its ID.

        Args:
            id (string): The ID of the file to fetch.

        Returns:
            dict: A dictionary containing the file record's details.
        """
        self.cursor.execute("SELECT * FROM files WHERE id = %s",[id])
        res = self.cursor.fetchone()
        return {"id":res[0],"name":res[1],"data":res[2],"creationTime":res[3],"modifiedTime":res[4],"uploader":res[5],"session":res[6],"emphemeral":res[7]}
    
    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.conn.close()
