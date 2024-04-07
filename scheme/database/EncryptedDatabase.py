import os
import sqlite3

# Class to support database operations
class EncryptedDatabase:
    # Constructor
    def __init__(self, reset=False):
        if reset == True and os.path.exists('eDatabase.db'):
            os.remove('eDatabase.db')
        self.conn = sqlite3.connect('eDatabase.db')

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
        print('Run sql command for createtable')
        # print("Run sql command:", sqlCommand)
        self.conn.execute(sqlCommand)
        # Commit transaction
        self.conn.commit()

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
        print('Run sql command for insertintotable')
        # print("Run sql command:", sqlCommand)
        self.conn.execute(sqlCommand)
        self.conn.commit()

    # This method retrieves all entries from a table
    def retrieveRecords(self, name, records: list):
        sqlRecords = str(records).strip('[]')
        
        sqlCommand = f"SELECT * FROM _{name} WHERE recordID IN ({sqlRecords});"
        print('Run sql command for retrieverecords')
        # print("I saw that you ran this command!!!! >:))))", sqlCommand)
        entries = self.conn.execute(sqlCommand).fetchall()
        return entries
    

    def getTableRecordLength(self, tableName):
        entries = self.conn.execute(f"SELECT * FROM _{tableName}").fetchall()
        return len(entries)
    
    # This method checks if an entry already exists within a table
    def check_entry(self, table, attribute, entry):
        val = self.conn.execute("""SELECT EXISTS(SELECT 1 FROM %s WHERE %s.%s='%s')""" % (table, table, attribute, entry)).fetchall()
        exists = int(val[0][0])
        return exists
    
    # This method deletes an entry from a table
    def delete_entry(self, table, attribute, entry):
        self.conn.execute("DELETE from %s WHERE %s.%s='%s'" % (table, table, attribute, entry))
        # Commit transaction
        self.conn.commit()

    def getAttributes(self):
        cur = self.conn.execute("SELECT * FROM Molecules")
        attr = list(map(lambda x: x[0], cur.description))
        return attr
    
    