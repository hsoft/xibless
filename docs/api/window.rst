Window
======

Technically, the ``Window`` is a :class:`View` subclass, but only because of it ``x``, ``y``,
``width`` and ``height`` properties (in fact, I should probably change that). The layout methods
don't make sense for the window because it doesn't have a superview. It represents, of course,
Cocoa's ``NSWindow``.

.. class:: Window(width, height, title)
    
    :param width: Numeric. See :attr:`View.width`.
    :param height: Numeric. See :attr:`View.height`.
    :param title: String. See :attr:`title`.
    
    .. attribute:: xProportion
    .. attribute:: yProportion
    
        *Numeric*. ``x`` and ``y`` coordinates in proportion of the main screen frame. This value
        has to be between 0.0 and 1.0.
    
    .. attribute:: title
        
        *String*. The text on the window. Equivalent to ``[self title]``.
    
    .. attribute:: canClose
    .. attribute:: canResize
    .. attribute:: canMinimize
        
        *Boolean*. Adjusts the window's ``style`` flags according to boolean values you set in those
        3 attributes. The behave the same way as the Close, Resize and Minimize checkboxes in
        Interface Builder.
    
    .. attribute:: initialFirstResponder
        
        See :class:`View`. Equivalent to ``[self initialFirstResponder]``.
    
    .. attribute:: autosaveName
        
        *String*. Equivalent to ``[self frameAutosaveName]``.
    
    .. attribute:: minSize
        
        :class:`Size`. Equivalent to ``[self minSize]``.
    
    .. attribute:: maxSize
        
        :class:`Size`. Equivalent to ``[self maxSize]``.

Panel
-----

Sublclasses :class:`Window` and represents Cocoa's ``NSPanel``.

.. class:: Panel(width, height, title)
    
    Same initializer as :class:`Window`
    
    .. attribute:: style
        
        One of :ref:`panel-style-constants`. Sets the style of the panel like IB's selector does.
    
