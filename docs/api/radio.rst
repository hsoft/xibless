RadioButtons
============

The ``RadioButtons`` class is a :class:`View` subclass which represents Cocoa's ``NSMatrix`` in
"radio" mode.

.. class:: RadioButton(parent, items[, columns=1])
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param items: A list of strings. See :attr:`items`
    :param columns: Integer. See :attr:`columns`
    
    .. attribute:: items
        
        A list of strings determining the radio buttons that will be present in the matrix.
    
    .. attribute:: columns
        
        By setting this attribute to something larger than 1, you can make radio buttons span over
        multiple columns. The number of rows will be automatically calculated from the number of
        items. 
        
        The cells in the array are row-ordered, that is, the first row of cells appears
        first in the array, followed by the second row, and so forth.
        
        **Warning**. The number of items has to fit exactly in the square that is formed by the
        rows and columns. For example, if you have 3 columns, your number of items have to be a
        multiple of 3.
