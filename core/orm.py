"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import copy
import zope.interface
import MySQLdb
from iorm import *
from db import *

"""
" Abstract and base object.
" Should not be instantiated directly.
" Implements basic functionality to fetch and store data to DB using db module.
"""
class Orm( object ):
    zope.interface.implements( IOrm )

    """
    " @param dict Dictionary of fields. Key - field name, Value - field's value
    """
    def __init__( self, list = {} ):
        self._fields = {}
        for i in list:
            self.setAttribute( i, list[i] )

    """
    " Clears any assigned fields
    "
    " @return self
    """
    def _clear( self ):
       self._fields = {}

       return self

    """
    " Main point to fetch data from database.
    "
    " @param string where String condition
    " @return list List of instances of needed classes
    """
    def fetchObjects( self, where = None, limit = None, offset = None, orderByDict = None ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        sql = "SELECT * FROM {}".format( dTable )
        if where != None and len( where ) > 0:
            sql += " WHERE " + where

        if orderByDict != None:
            s = ", ".join( [ '%s %s' % ( k, v ) for ( k, v ) in orderByDict.items() ] )
            sql += " ORDER BY " + s

        if limit != None:
            ls = " LIMIT "
            limit = str( limit )
            offset = str( offset ) if offset != None else None
            lss = ls + limit if offset == None else ls + offset + ", " + limit
            sql += lss

        db = DB.get()
        cur = db.cursor()
        try:
            cur.execute( sql )
        except Exception:
            print "[SQL]: " + sql

        rows = cur.fetchall()
        fieldNames = [i[0] for i in cur.description]
        result = []
        for o in rows:
            c = copy.copy( self )
            c._clear()
            for i in xrange( len( o ) ):
                v = o[i]
                n = fieldNames[i]
                c.attr( n, v )

            result.append( c )

        return result

    """
    " Wrapper to fetch only one object by condition
    "
    " @return __CLASS__ An instance of needed class
    """
    def fetchObject( self, where = None ):
        l = self.fetchObjects( where, limit = 1 )

        return l[0] if len( l ) > 0 else None

    """
    " Wrapper to fetch only one object by increment field
    "
    " @return __CLASS__ An instance of needed class
    """
    def _fetchObjectByIncrementField( self, v ):
        where = self._getIncrementField() + '="' + self.escapeString( str( v ) ) + '"'

        return self.fetchObject( where )

    """
    " Returns incement field if exists
    "
    " @return str
    """
    def _getIncrementField( self ):
        return self._definition.incrementField

    """
    " @implements( IOrm )
    """
    def getAttribute( self, name ):
        try:
            v = self._fields[name]
        except KeyError, e:
            v = None;

        return v;

    """
    " @implements( IOrm )
    """
    def setAttribute( self, name, value ):
        name = self.escapeString( str( name ) )
        if isinstance( value, str ):
            value = self.escapeString( value )

        self._fields[name] = value

        return self;

    """
    " @implements( IOrm )
    """
    def attr( self, name, value = None ):
        return self.setAttribute( name, value ) if value else self.getAttribute( name )

    """
    " @implements( IPersistentObject )
    " @note Transaction unsafe
    """
    def insert( self ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        fieldList = dict( self._fields )

        if not fieldList:
            return self

        db = DB.get()
        cur = db.cursor()

        try:
            del fieldList[dInc]
        except KeyError:
            pass # Means no attribute provided

        kList = fieldList.keys()
        fields = ", ".join( kList )

        values = ", ".join( [ '"%s"' % ( v ) for ( k, v ) in fieldList.items() ] )
        sql = "INSERT INTO {} ({}) VALUES ({})".format( dTable, fields, values )
        cur.execute( sql )
        lastid = cur.lastrowid
        if dInc and lastid:
            self.setAttribute( dInc, lastid )
        cur.close()

        return self

    """
    " @implements( IOrm )
    " @note Transaction unsafe
    """
    def update( self ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        fieldList = dict( self._fields )
        if not fieldList:
            return self

        db = DB.get()
        cur = db.cursor()

        kList = fieldList.keys()
        values = ", ".join( [ '%s="%s"' % ( k, v ) for ( k, v ) in fieldList.items() ] )
        where = ""
        for k in dKeys:
            where += k + "=\"" + str( fieldList[k] ) + "\""

        sql = "UPDATE {} SET {} WHERE {}".format( dTable, values, where )
        cur.execute( sql )
        cur.close()

    """
    " Returns WHERE condition to check if current object exists in table
    "
    " @return bool
    """
    def _getExistCondition( self ):
        dKeys = self._definition.keys
        fieldList = dict( self._fields )
        where = []

        for k in dKeys:
            try:
                v = fieldList[k]
            except KeyError:
                continue

            where.append( k + "=\"" + str( fieldList[k] ) + "\"" )

        return " AND ".join( where ) if len( where ) else ""

    """
    " Checks if current object has been stored
    "
    " @return bool
    """
    def exists( self ):
        w = self._getExistCondition()
        if not len( w ):
            return False

        o = self.fetchObject( w )
        return bool( o )

    """
    " Wrapper to check if value is int
    "
    " @return bool
    """
    @staticmethod
    def _isInt( value ):
        if value == None:
            return False

        try:
            int( value )
            return True
        except ValueError:
            return False

    """
    " Checks if data has been assigned
    "
    " @return bool
    """
    def hasFields( self ):
        return bool( len( self._fields ) )


    """
    " Escapes characters to prevent sql inj
    "
    " @return str
    """
    @staticmethod
    def escapeString( s ):
        result = s.replace( "'", "\'" ).replace( "\"", "\\\"" )

        return result
