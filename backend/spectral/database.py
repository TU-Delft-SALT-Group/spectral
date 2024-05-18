import psycopg 
import uuid

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
    
    def store_transcription(self, file_id, file_transcription):
        """
        Stores a transcription record in the database.

        Args:
            file_id (string): The ID of the file associated with the transcription.
            file_transcription (list): A list of transcription entries to store, each containing "start", "end", and "value" keys.
        """
        file_transcription_id = str(uuid.uuid4())
        self.cursor.execute("""
                            INSERT INTO file_transcription (id, file)
                            VALUES (%s, %s);
                            """,[file_transcription_id,file_id])
        for transcription in file_transcription:
            self.cursor.execute("""
                            INSERT INTO transcription (id, file_transcription, start, "end", value)
                            VALUES (%s, %s, %s, %s, %s);
                            """,[str(uuid.uuid4()),file_transcription_id,transcription["start"],transcription["end"],transcription["value"]])
    
    def get_transcriptions(self, file_id):
        """
        Fetches transcriptions associated with a file from the database.

        Args:
            file_id (string): The ID of the file to fetch transcriptions for.

        Returns:
            list: A list of lists containing transcription entries, where each inner list represents a file transcription and contains dictionaries with "start", "end", and "value" keys.
        """
        self.cursor.execute("""
                           SELECT id FROM file_transcription
                           WHERE file = %s 
                           """,[file_id])
        file_transcriptions = self.cursor.fetchall()
        res = []
        for file_transcription in file_transcriptions:
            self.cursor.execute("""
                           SELECT start, "end", value FROM transcription
                           WHERE file_transcription = %s 
                           """,[file_transcription[0]])
            transcriptions = self.cursor.fetchall()
            parsed_file_transcriptions = []
            for transcription in transcriptions:
                parsed_file_transcriptions.append({"start":transcription[0],"end":transcription[1],"value":transcription[2]})
            res.append(parsed_file_transcriptions)
        return res
    
    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.conn.close()