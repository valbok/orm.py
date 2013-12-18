"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import MySQLdb
import unittest
from core import *

class DBTest( unittest.TestCase ):
    def testInitUnknownDB( self ):
        with self.assertRaises( MySQLdb.OperationalError ):
            DB.init( db = "unknownDatabase" )

    def testInitKnownDB( self ):
        DB.init( db = "mysql" )

    def testGetNotInitialized( self ):
        DB.uninit()
        with self.assertRaises( AttributeError ):
            db = DB.get()

    def testGetInitialized( self ):
        DB.init( db = "mysql" )
        db = DB.get()
        self.assertEquals( True, isinstance( db, MySQLdb._mysql.connection ) )

if __name__ == '__main__':
    unittest.main()
