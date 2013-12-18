"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import MySQLdb

"""
" MySQL Database handler
" Used to initialize database connection and keep it for whole process
" Implements kind of singelton
"
" Usage:
"    DB.init( db = "databasename" )
"    db = DB.get()
"    cur = db.currsor
"    cur.execute( "SHOW TABLES" )
"""
class DB( object ):

    """
    " Static instance of current class
    """
    _instance = None

    """
    " @param MySQLdb._mysql.connection Stores database connection to current object
    """
    def __init__( self, db ):
        self._db = db

    @property
    def db( self ):
        return self._db

    """
    " It should be called before use of DB.get()
    "
    " @return MySQLdb._mysql.connection
    """
    @staticmethod
    def init( host = "localhost", user = "root", passwd = "", db = "" ):
        DB._instance = DB( MySQLdb.connect( host, user, passwd, db ) )

        return DB._instance

    """
    " Returns static instance that was stored in DB.init()
    "
    " @return __CLASS__
    """
    @staticmethod
    def get():
        return DB._instance.db;

    """
    " Unbinds previously stored instance
    "
    " @return void
    """
    @staticmethod
    def uninit():
        DB._instance = None
