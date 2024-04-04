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
    def executeCreationCommand(self, sql):
        """
        use this for creating stuff
        """
        self.conn.execute(sql)
        # Commit transaction
        self.conn.commit()

    # This method retrieves all entries from a table
    def retrieveRecords(self, sql):
        entries = self.conn.execute(sql).fetchall()
        return entries
    
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
    
    