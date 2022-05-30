# Connect to MYSQL Database

#import mysql.connector as myql
import mysql
from mysql import connector
from mysql.connector import Error

class App:
    def db_conn(self):
        try:
            h_db = mysql.connector.connect(host="localhost", username="root", password="risi", database="HPS",
                                           buffered=True)
            h_cursor = h_db.cursor()
        except mysql.connector.Error as error:
            print("Query Failed {}".format(error))
        return h_db,h_cursor

AppInst = App()
