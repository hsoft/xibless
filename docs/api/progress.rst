ProgressIndicator
=================

The ``ProgressIndicator`` is a :class:`View` subclass that represents Cocoa's ``NSProgressIndicator``.

.. class:: ProgressIndicator(parent)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    
    .. attribute:: style
        
        :ref:`Cocoa constant <literal-consts>`. The type of the indicator. Equivalent to
        ``[self style]``. Use with ``NSProgressIndicatorStyle`` constants.
    
    .. attribute:: minValue
        
        Numeric. Minimum value of the indicator. Equivalent to ``[self minValue]``.
    
    .. attribute:: maxValue
        
        Numeric. Maximum value of the indicator. Equivalent to ``[self maxValue]``.
    
    .. attribute:: value
        
        Numeric. Current value of the indicator. Equivalent to ``[self doubleValue]``.
    
    .. attribute:: indeterminate
        
        Boolean. Whether the indicator has a determinate progress value. Equivalent to
        ``[self isDeterminate]``.
    
    .. attribute:: displayedWhenStopped
        
        Boolean. Whether the indicator displays its progress when not animated. Equivalent to
        ``[self isDisplayedWhenStopped]``.
    

