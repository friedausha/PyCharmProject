import mysql.connector
class Database:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="kumparan-data-mysql.cgnxdvloq0ms.ap-southeast-1.rds.amazonaws.com",
            user="kumkum",
            passwd="Kumparan12304",
            database="kawalpemilu"
        )

    def __del__(self):
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        table = "CREATE TABLE IF NOT EXISTS hasil (prabowo INTEGER, jokowi INTEGER , suara_sah INTEGER , suara_tidak_sah INTEGER )"
        cursor.execute(table)

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()