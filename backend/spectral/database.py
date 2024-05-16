import psycopg 

class Database:
    def __init__(self, user, password, host, port, dbname):
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
        self.cursor.execute("SELECT * FROM files WHERE id = %s",[id])
        res = self.cursor.fetchone()
        return {"id":res[0],"name":res[1],"data":res[2],"creationTime":res[3],"modifiedTime":res[4],"uploader":res[5],"session":res[6],"emphemeral":res[7]}
    
    def close(self):
        self.cursor.close()
        self.conn.close()
