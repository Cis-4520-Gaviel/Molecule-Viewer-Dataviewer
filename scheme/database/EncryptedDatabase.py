import os
import sqlite3
import time

# Class to support database operations
class EncryptedDatabase:
    """
    A basic database wrapper for an sqlite database. Although it is encrypted it can support the plain data as well. 
    """
    # Constructor
    def __init__(self, reset=False):
        if reset == True and os.path.exists('data/eDatabase.db'):
            os.remove('data/eDatabase.db')
        self.conn = sqlite3.connect('data/eDatabase.db')
    def _logAction(self, sqlAction, loggedTime):
        f = open("data/queriesLogged.txt", "a")
        f.write("[" + time.ctime(loggedTime) +"]: " + sqlAction)
        f.write("\n")
        f.close()

    # This method creates tables
    def createTable(self, name, attributes):
        """
        use this for creating stuff
        """
        sqlAttributes = "( recordID INT"
        for attribute in attributes:
            sqlAttributes = sqlAttributes + f", _{attribute} VARCHAR(120)"
        sqlAttributes = sqlAttributes + ")"

        sqlCommand = f"""CREATE TABLE IF NOT EXISTS _{name} {sqlAttributes};"""

        logTime = time.time()
        self.conn.execute(sqlCommand)
        # Commit transaction
        self.conn.commit()
        self._logAction(sqlCommand, logTime)

    def insertIntoTable(self, name, attributes, values):
        sqlAttributes = "( recordID"
        for attribute in attributes:
            sqlAttributes = sqlAttributes + f", _{attribute}"
        sqlAttributes = sqlAttributes + ")"

        sqlValues = f"{values[0]}"
        for value in values[1:]:
            sqlValues = sqlValues + f",'{value}'"
        
        
        sqlCommand = f"""INSERT OR IGNORE
                            INTO _{name} {sqlAttributes}
                            VALUES ({sqlValues});"""
        logTime = time.time()

        self.conn.execute(sqlCommand)
        self.conn.commit()
        self._logAction(sqlCommand, logTime)

    # This method retrieves all entries from a table
    def retrieveRecords(self, name, records: list):
        sqlRecords = str(records).strip('[]')

        sqlCommand = f"SELECT * FROM _{name} WHERE recordID IN ({sqlRecords});"

        logTime = time.time()
        entries = self.conn.execute(sqlCommand).fetchall()
        self._logAction(sqlCommand, logTime)
        return entries
    

    def getTableRecordLength(self, tableName):
        logTime = time.time()
        entries = self.conn.execute(f"SELECT * FROM _{tableName}").fetchall()

        self._logAction(f"SELECT * FROM _{tableName}", logTime)

        return len(entries)