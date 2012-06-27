Window
======

Technically, the ``Window`` is a :class:`View` subclass, but only because of it ``x``, ``y``,
``width`` and ``height`` properties (in fact, I should probably change that). The layout methods
don't make sense for the window because it doesn't have a superview. It represents, of course,
Cocoa's ``NSWindow``.

.. class:: Window(x, y, width, height, title)
    
    :param x: Numeric. See :attr:`View.x`.
    :param y: Numeric. See :attr:`View.y`.
    :param width: Numeric. See :attr:`View.width`.
    :param height: Numeric. See :attr:`View.height`.
    :param title: String. See :attr:`title`.
    
    .. attribute:: title
        
        *String*. The text on the window. Equivalent to ``[self title]``.
