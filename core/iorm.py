"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from abc import ABCMeta, abstractmethod, abstractproperty
import zope.interface

"""
" Interface of any persistent objects
"""
class IOrm( zope.interface.Interface ):
    """
    " Dictionary of fields
    "
    " @var dict
    """
    _fields = zope.interface.Attribute( """Field List""" )

    """
    " Metadata of current object
    "
    " @var Definition
    """
    _definition = zope.interface.Attribute( """DB Definition""" )

    """
    " Returns attribute value
    "
    " @return any
    """
    def getAttribute():
        pass

    """
    " Assigns attribute value
    "
    " @return self
    """
    def setAttribute():
        pass

    """
    " Stores current object
    "
    " @return self
    """
    def insert():
        pass

    """
    " Updates current object
    "
    " @return self
    """
    def update():
        pass

    """
    " Wrapper to setAttribute and getAtribute
    "
    " @return any
    """
    def attr():
        pass
