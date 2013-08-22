#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Atom, Typed
from atom.datastructures.api import sortedmap


class ReadHandler(Atom):
    """ A base class for defining expression read handlers.

    """
    def __call__(self, owner, name):
        """ Evaluate and return the expression value.

        This method must be implemented by subclasses.

        Parameters
        ----------
        owner : Declarative
            The declarative object on which the expression should
            execute.

        name : str
            The attribute name on the declarative object for which
            the expression is providing a value.

        """
        raise NotImplementedError


class WriteHandler(Atom):
    """ A base class for defining expression write handlers.

    """
    def __call__(self, owner, name, change):
        """ Write the change to the expression.

        This method must be implemented by subclasses.

        Parameters
        ----------
        owner : Declarative
            The declarative object on which the expression should
            execute.

        name : str
            The attribute name on the declarative object for which
            the expression is providing a value.

        change : dict
            The change dict generated by the declarative object.

        """
        raise NotImplementedError


class ExpressionEngine(Atom):
    """ A class which manages reading and writing bound expressions.

    """
    #: A mapping of string name to read handler.
    read_handlers = Typed(sortedmap, ())

    #: A mapping of string name to list of write handlers.
    write_handlers = Typed(sortedmap, ())

    def read(self, owner, name):
        """ Compute and return the value of an expression.

        Parameters
        ----------
        owner : Declarative
            The declarative object which owns the engine.

        name : str
            The name of the relevant bound expression.

        """
        return self.read_handlers[name](owner, name)

    def write(self, owner, name, change):
        """ Write a change to an expression.

        Parameters
        ----------
        owner : Declarative
            The declarative object which owns the engine.

        name : str
            The name of the relevant bound expression.

        change : dict
            The change dictionary generated by the declarative object
            which owns the engine.

        """
        for handler in self.write_handlers[name]:
            handler(owner, name, change)

    def copy(self):
        """ Create a copy of the expression engine.

        Returns
        -------
        result : ExpressionEngine
            A copy of the engine with independent handler maps.

        """
        new = ExpressionEngine()
        new.read_handlers = self.read_handlers.copy()
        new.write_handlers = w = sortedmap()
        for key, value in self.write_handlers.items():
            w[key] = value[:]
        return new
