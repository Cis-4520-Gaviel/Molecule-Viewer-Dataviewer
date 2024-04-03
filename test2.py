import sqlite3;
import os;
import MolDisplay;
import molecule;
class Database:
    """
    A database class to store molecules
    """
    def __init__(self, reset=False):
        if reset==True:
            if os.path.exists('molecules.db'):
                os.remove('molecules.db');
        self.conn = sqlite3.connect('molecules.db');
    
        self.create_tables();

        
    def create_tables(self):
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements ( 
             		ELEMENT_NO   INTEGER NOT NULL,
             		ELEMENT_CODE       VARCHAR(3) NOT NULL,
             		ELEMENT_NAME    VARCHAR(32) NOT NULL,
             		COLOUR1    CHAR(6) NOT NULL,
             		COLOUR2    CHAR(6) NOT NULL,
             		COLOUR3    CHAR(6) NOT NULL,
             	    RADIUS    DECIMAL(3) NOT NULL,
             		PRIMARY KEY (ELEMENT_CODE) );""" );
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms (
                    ATOM_ID         INTEGER         NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ELEMENT_CODE    VARCHAR(3)      NOT NULL,
                    X               DECIMAL(7,4)    NOT NULL,
                    Y               DECIMAL(7,4)    NOT NULL,
                    Z               DECIMAL(7,4)    NOT NULL);""");
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds(
                    BOND_ID     INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
                    A1          INTEGER NOT NULL,
                    A2          INTEGER NOT NULL,
                    EPAIRS      INTEGER NOT NULL);""");
        
        self.conn.execute("""   CREATE TABLE IF NOT EXISTS Molecules(
                    MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    NAME        TEXT UNIQUE);""");
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom(
                    MOLECULE_ID INTEGER NOT NULL,
                    ATOM_ID     INTEGER NOT NULL,
                    PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                    FOREIGN KEY (ATOM_ID) REFERENCES Atoms); """);
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond(
                    MOLECULE_ID INTEGER NOT NULL,
                    BOND_ID     INTEGER NOT NULL,
                    PRIMARY KEY (MOLECULE_ID, BOND_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                    FOREIGN KEY (BOND_ID) REFERENCES Bonds); """);
        self.conn.commit()
    
    def __setitem__(self, table, values):
        self.conn.execute(f"""INSERT OR IGNORE INTO {table}
                    VALUES {values};""");
        self.conn.commit();
    
    def add_atom(self, molname, atom):
        cursor = self.conn.cursor();
        cursor.execute(f"""INSERT OR IGNORE INTO Atoms(ELEMENT_CODE, X, Y, Z)
                    VALUES ('{atom.element}', {atom.x}, {atom.y}, {atom.z});""")
        atomId = cursor.lastrowid;
        moleculeRow = self.conn.execute(f"""SELECT MOLECULE_ID FROM Molecules
                                WHERE NAME='{molname}';""").fetchall();
        self.conn.execute(f"""INSERT OR IGNORE INTO MoleculeAtom
                        VALUES( {moleculeRow[0][0]}, {atomId}); """);

    def add_bond(self, molname, bond):
        cursor = self.conn.cursor();
        cursor.execute(f"""INSERT OR IGNORE INTO Bonds(A1,A2,EPAIRS)
                    VALUES ({bond.a1}, {bond.a2}, {bond.epairs});""")
        bondId = cursor.lastrowid;
        moleculeRow = self.conn.execute(f"""SELECT MOLECULE_ID FROM Molecules
                                WHERE NAME='{molname}';""").fetchall();
        self.conn.execute(f"""INSERT OR IGNORE INTO MoleculeBond
                        VALUES ({moleculeRow[0][0]}, {bondId});  """);
    
    def add_molecule(self, name, fp):
        try:
            mol = MolDisplay.Molecule()
            mol.parse(fp);
            self.conn.execute(f"""INSERT OR IGNORE INTO Molecules(NAME)
                        VALUES ('{name}');""");
            for x in range(mol.atom_no):
                self.add_atom(name, mol.get_atom(x));
            for x in range(mol.bond_no):
                self.add_bond(name, mol.get_bond(x));
            self.conn.commit();
            return True
        except:
            self.conn.rollback();
            return False
    def add_molecule_str(self, name, molStr):
        try:
            mol = MolDisplay.Molecule()
            mol.parseString(molStr);
            self.conn.execute(f"""INSERT OR IGNORE INTO Molecules(NAME)
                        VALUES ('{name}');""");
            for x in range(mol.atom_no):
                self.add_atom(name, mol.get_atom(x));
            for x in range(mol.bond_no):
                self.add_bond(name, mol.get_bond(x));
            self.conn.commit();
            return True
        except Exception as e:
            print(e)
            self.conn.rollback();
            return False
    
    def load_mol(self, name):
        mol = MolDisplay.Molecule();
        atoms = self.conn.execute(f"""SELECT Atoms.* FROM 
                            Atoms INNER JOIN MoleculeAtom ON (Atoms.ATOM_ID=MoleculeAtom.ATOM_ID)
                            INNER JOIN Molecules ON (MoleculeAtom.MOLECULE_ID=Molecules.MOLECULE_ID)
                            WHERE Molecules.NAME='{name}';""" ).fetchall();
        for atom in atoms:
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])

        bonds = self.conn.execute(f"""SELECT Bonds.* FROM 
                            Bonds INNER JOIN MoleculeBond ON (Bonds.BOND_ID=MoleculeBond.BOND_ID)
                            INNER JOIN Molecules ON (MoleculeBond.MOLECULE_ID=Molecules.MOLECULE_ID)
                            WHERE Molecules.NAME='{name}';""" ).fetchall();
        for bond in bonds:
            mol.append_bond(bond[1], bond[2], bond[3])
        return mol
    def load_allMol(self):
        """
        Returns a array of dictionaries for molecules. Includes database id, name, atoms, bonds
        """
        mols = self.conn.execute("""
            SELECT Molecules.NAME, Molecules.MOLECULE_ID FROM Molecules;
        """).fetchall();
        moleculeList = [];
        for mol in mols:
            molObj = self.load_mol(mol[0]);
            moleculeList.append({'name': mol[0],
                       'id': mol[1],
                       'atom_count': molObj.atom_no,
                       'bond_count': molObj.bond_no})
        return moleculeList;
    
    def radius(self):
        elements = self.conn.execute(f"""SELECT Elements.ELEMENT_CODE, Elements.RADIUS FROM 
                            Elements;""" ).fetchall();
        newDict = {}
        print(elements)
        for radius in elements:
            newDict[radius[0]] = radius[1]
        return newDict
    
    def element_name(self):
        elements = self.conn.execute(f"""SELECT Elements.ELEMENT_CODE, Elements.ELEMENT_NAME FROM 
                            Elements;""" ).fetchall();
        newDict = {}
        for name in elements:
            newDict[name[0]] = name[1]
        return newDict
    
    def radial_gradients(self):
        elements = self.conn.execute(f"""SELECT Elements.ELEMENT_NAME, Elements.COLOUR1,Elements.COLOUR2,Elements.COLOUR3 FROM 
                            Elements;""" ).fetchall();
        svgString = ""
        print(elements)
        for radius in elements:
            svgString+= f"""
                <radialGradient id="{radius[0]}" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                <stop offset="0%" stop-color="#{radius[1]}"/>
                <stop offset="50%" stop-color="#{radius[2]}"/>
                <stop offset="100%" stop-color="#{radius[3]}"/>
                </radialGradient>""";
        svgString+= f"""
                <radialGradient id="default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                <stop offset="0%" stop-color="#FF00FF"/>
                <stop offset="50%" stop-color="#8C018C"/>
                <stop offset="100%" stop-color="#140014"/>
                </radialGradient>""";
        
        return svgString
    def getElementsJSON(self):
        list = [];
        elements = self.conn.execute(f"""SELECT Elements.ELEMENT_CODE, Elements.ELEMENT_NAME,Elements.COLOUR1,Elements.COLOUR2, Elements.COLOUR3, Elements.RADIUS FROM 
                            Elements;""" ).fetchall();
        for element in elements:
            elementObj = {}
            elementObj['code'] = element[0];
            elementObj['name'] = element[1];
            elementObj['colour1'] = element[2];
            elementObj['colour2'] = element[3];
            elementObj['colour3'] = element[4];
            elementObj['radius'] = element[5];
            list.append(elementObj);
        return list;
    def deleteEntry(self, table, identifier, name):
        print("WE HAVE DELETED SOMETIHNG")

        count = self.conn.execute(f""" SELECT COUNT(*) FROM {table} WHERE {identifier}={name};""").fetchone();
        if(count[0] == 0):
            return False, True
        print("WE HAVE DELETED SOMETIHNG2")

        self.conn.execute(f""" DELETE FROM {table} WHERE {identifier}={name};""")
        count = self.conn.execute(f""" SELECT COUNT(*) FROM {table} WHERE {identifier}={name};""").fetchone();
        self.conn.commit();
        print(count)
        if(count[0] == 0):
            return True, True
        else:
            return False, False
    def delete_molecule(self, name):
        count = self.conn.execute(f""" SELECT COUNT(*) FROM Molecules WHERE Molecules.NAME='{name}';""").fetchone();
        if count == 0:
            return False
        try:
            self.conn.execute(f"""DELETE FROM Atoms WHERE EXISTS
                            (SELECT * FROM MoleculeAtom INNER JOIN Molecules ON MoleculeAtom.MOLECULE_ID=Molecules.MOLECULE_ID
                                WHERE Molecules.NAME='{name}' AND MoleculeAtom.ATOM_ID=Atoms.ATOM_ID);""" );
            self.conn.execute(f"""DELETE FROM Bonds WHERE EXISTS
                            (SELECT * FROM MoleculeBond INNER JOIN Molecules ON MoleculeBond.MOLECULE_ID=Molecules.MOLECULE_ID
                                WHERE Molecules.NAME='{name}' AND MoleculeBond.BOND_ID=Bonds.BOND_ID);""" );
            self.conn.execute(f"""DELETE FROM
                                MoleculeAtom WHERE EXISTS 
                                (SELECT * FROM Molecules WHERE Molecules.NAME='{name}' AND MoleculeAtom.MOLECULE_ID=Molecules.MOLECULE_ID);""")
            self.conn.execute(f"""DELETE FROM
                                MoleculeBond WHERE EXISTS 
                                (SELECT * FROM Molecules WHERE Molecules.NAME='{name}' AND MoleculeBond.MOLECULE_ID=Molecules.MOLECULE_ID);""")
            self.conn.execute(f""" DELETE FROM Molecules WHERE Molecules.NAME='{name}';""")
            self.conn.commit();
            return True
        except Exception as e:
            print(e);
            self.conn.rollback();
            return False

if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    fp = open( 'water-3D-structure-CT1000292221.sdf' );
    db.add_molecule( 'Water', fp );
    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    db.add_molecule( 'Caffeine', fp );
    fp = open( 'CID_31260.sdf' );
    db.add_molecule( 'Isopentanol', fp );
    fp = open('Romanium.sdf');
    db.add_molecule( 'Romanium', fp );

    # display tables
    #  print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    #  print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    #  print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    #  print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    #  print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    #  print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );
    db.radius();
    MolDisplay.radius = db.radius();
    MolDisplay.element_name = db.element_name();
    MolDisplay.header += db.radial_gradients();
    
    molculeList = db.load_allMol();
    for name in molculeList:
        print(name);

    

    # db.delete_molecule('Water')
    # molculeList = db.load_allMol();
    # for name in molculeList:
    #     print(name);
    #db.deleteEntry('Elements','ELEMENT_CODE',"'H'")
    # mol = db.load_mol( 'Caffeine' );
    # thing = MolDisplay.Rotation()
    # fp = open( "test/thing.svg", "w+" );
    # fp.write( mol.svg(True) );
    # fp.close();
    # thing.loadMol(mol);
    # for x in range(72):
    #     fp = open( "test/thing"+ str(x) + ".svg", "w+" );
    #     fp.write( thing.getRotation(x,0,0) );
    #     fp.close();
    
    # for molc in ['Water', 'Caffeine', 'Isopentanol' , 'Romanium']: #'Water', 'Caffeine', 'Isopentanol' , 
    #     mx = molecule.mx_wrapper(5,0,0);
    #     mol = db.load_mol( molc );
    #     fp = open( molc + "-original.svg", "w+" );
    #     fp.write( mol.svg(nightmare=True) );
    #     fp.close();
    #     mol.xform( mx.xform_matrix );
    #     fp = open( molc + ".svg", "w+" );
    #     fp.write( mol.svg(nightmare=True) );
    #     fp.close();
