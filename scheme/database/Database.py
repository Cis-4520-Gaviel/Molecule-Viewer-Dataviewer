import os
import sqlite3

# Class to support database operations
class Database:

    # Constructor
    def __init__(self, reset=False):
        if reset == True and os.path.exists('molecules.db'):
            os.remove('molecules.db')
        self.conn = sqlite3.connect('molecules.db')

    # This method creates tables
    def create_tables(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules 
                        (   NAME            TEXT            NOT NULL,
                            ATOM_NO         INTEGER         NOT NULL,
                            BOND_NO         INTEGER         NOT NULL)""")
        # Commit transaction
        self.conn.commit()

    # This method adds a molecule to the Molecules table
    def add_molecule(self, name, atom_no, bond_no):
        self.conn.execute("""INSERT OR IGNORE
                            INTO Molecules (NAME, ATOM_NO, BOND_NO)
                            VALUES ('%s', %s, %s)""" % (name, atom_no, bond_no))
        # Commit transaction
        self.conn.commit()
    
    # This method retrieves all entries from a table
    def retrieve_all(self, table):
        entries = self.conn.execute("SELECT * FROM %s" % table).fetchall()
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
    
    