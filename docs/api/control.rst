Control
=======

The ``Control`` is a :class:`View` subclass which represents Cocoa's ``NSControl``.

.. class:: Control(parent, width, height)

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param width: Numeric. See :attr:`View.width`.
    :param height: Numeric. See :attr:`View.height`.
    
    .. attribute:: font
        
        :class:`Font`. The font of the control. Equivalent to ``[self font]``.
    
    .. attribute:: controlSize
        
        :ref:`Cocoa constant <literal-consts>`. One of the 3 Regular, Small and Mini pre-defined
        control size. Setting this attribute will change the font size and height of the control
        to pre-defined values (like Interface Bulder does). Use with ``NSControlSize`` constants.
    
