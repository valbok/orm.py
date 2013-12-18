"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

"""
" Class to define meta data about objects
"""
class Definition( object ):

    """
    " @param string table Name of table
    " @param list keys List of keys which will be used to store object
    " @param string incrementField Name of increment field to skip it from inserts
    """
    def __init__( self, table, keys, incrementField = None ):
        self._table = table
        self._keys = keys
        self._incrementField = incrementField

    @property
    def table( self ):
        return self._table

    @property
    def keys( self ):
        return self._keys

    @property
    def incrementField( self ):
        return self._incrementField
