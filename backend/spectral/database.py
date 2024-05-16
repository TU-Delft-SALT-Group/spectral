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
        self.cursor.execute("SELECT * FROM files")
        res = self.cursor.fetchone()
        print(res)
        # self.cursor.execute("SELECT * FROM files WHERE id = %s",id)
        return {"name":res[0],"data":res[2]}
        # with open("/backend/tests/data/torgo-dataset/MC02_control_head_sentence1.wav", 'rb') as fd:
        #     contents = fd.read()  
        # return {"data":contents}
    
    def close(self):
        self.cursor.close()
        self.conn.close()
