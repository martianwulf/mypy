#! python34
import mysql.connector
from mysql.connector import Error
import os.path, csv, re

date_pattern = r"^\d{4}-\d{2}-\d{2}$"

class mydbException(Exception):
    pass

class mysqlDb:
    def __init__(self, host, user, pwd, dbname):
        '''Creates a mysql dbase class object'''
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname
        self.conn = None
    def connect(self):
        '''Connects to a mysql database using member variables'''
        self.conn = mysql.connector.connect(host=self.host,
                                            database=self.dbname,
                                            user = self.user,
                                            password=self.pwd)
    def closeConnection(self):
        '''Closes the mysql connection'''
        if self.conn.is_connected():
            self.conn.close()
    def cursor(self,buffered=None,raw=None,prepared=None,cursor_class=None):
        '''returns a mysql cursor object'''
        return self.conn.cursor(buffered,raw,prepared,cursor_class)
    def commit(self):
        '''Commit current transaction'''
        self.conn.commit()
    def getTableCols(self, tableName):
        '''Returns a list of columns in tablename'''
        curr = self.cursor()
        q = "select column_name from information_schema.columns where table_name = '{}'".format(tableName)
        curr.execute(q)
        col_list = []
        while True:
            row = curr.fetchone()
            if row is None:
                break
            col_list.append(row[0])
        return col_list
    def getTableCols2(self, tableName):
        '''Returns a list of list of columns in tablename and their types etc'''
        curr = self.cursor()
        q = "show columns in {}".format(tableName)
        curr.execute(q)
        col_data = []
        while True:
            row = curr.fetchone()
            if row is None:
                break
            col_data.append(row)
        return col_data
    def isTable(self, dbasename, tablename):
        '''Check if tablename exists in a database'''
        curr = self.cursor()
        queryTables = "select table_name from information_schema.tables where table_schema = '{}' and table_name = '{}'"
        
        curr.execute(queryTables.format(dbasename, tablename))
        row = curr.fetchone()
        if row is None:
            return False
        else:
            return True
        
    def csvExport(self, tablename, outfile):
        '''Exports a table as a csv file'''
        if not self.isTable(tablename):
            raise mydbException("Cannot find table {} in dbase".format(tablename))
        d, f = os.path.split(outfile)
        if os.path.isfile(outfile) or not os.path.isdir(d):
            print('Export failed')
            raise mydbException("Invalid file name")
        col_names = []
        curr = self.cursor()
        curr.execute("select column_name from information_schema.columns where table_name = '{}'".format(tablename))
        while True:
            row = curr.fetchone()
            if row is None:
                break
            else:
                col_names.append(row[0])
        with open(outfile, 'w', newline = '') as f:
            csvwrtr = csv.writer(f)
            csvwrtr.writerow(col_names)
            curr.execute('select * from {}'.format(tablename))
            row = curr.fetchone()
            while row is not None:
                csvwrtr.writerow(row)
                row = curr.fetchone()
        print('Table {} successfully exported to directory: {}'.format(tablename,os.path.split(outfile)[0]))
    
    def csvImport(self, tablename, infile):
        if not self.isTable(tablename):
            raise Exception("Cannot find table {} in dbase".format(tableName))
        ext = os.path.splitext(infile)[1]
        if 'csv' not in ext:
            print('Outfile ext not "csv"')
            return
        if not os.path.isfile(infile):
            print('Cannot open file "{}"'.format(infile))
            return
        extract_list = []
        with open(infile) as f:
            csvrdr = csv.reader(f)
            for row in csvrdr:
                if csvrdr.line_num == 1:
                    header = row
                    continue
                extract_list.append(row)
            print(header)
        for line in extract_list:
            innerlist = []
            q = "insert into {}(".format(tablename)+", ".join(header)+") values('"+"', '".join(line)+"')"
            curr = self.cursor()
            curr.execute(q)
        self.commit()
    
    def cloneTable(self, tableName, newTable):
        '''Create a new table with the same fields as tableName'''
        if not self.isTable(tableName):
            raise Exception("Cannot find table {} in dbase".format(tableName))
        if tableName == newTable:
            raise Exception('new table has the same name as original table')
        curr = self.cursor()
        #new 03/28/17
        cloneQuery = "create table {} like {}".format(newTable, tableName)
        curr.execute(cloneQuery)
        self.commit()
        
    def copyTable(self, fromTable, toTable):
        if not self.isTable(fromTable) and not self.isTable(toTable):
            print('Copy failed. Invalid table')
            return
        fromCols = self.getTableCols(fromTable)
        toCols = self.getTableCols(toTable)
        if len(fromCols) != len(toCols):
            print('Copy failed. Unequal tables')
            return
        