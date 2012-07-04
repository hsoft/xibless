Button
======

The ``Button`` is a :class:`View` subclass which represents Cocoa's ``NSButton``.

.. class:: Button(parent, title[, action=None])

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param title: A string. See :attr:`title`.
    :param action: An :class:`Action`. See :attr:`action`.
    
    .. attribute:: buttonType
    
        :ref:`Cocoa constant <literal-consts>`. The type of the button. Equivalent to
        ``[self buttonType]``. Use with ``NSButtonType`` constants.
    
    .. attribute:: bezelStyle
    
        :ref:`Cocoa constant <literal-consts>`. The style of the button. Equivalent to
        ``[self bezelStyle]``. Use with ``NSBezelStyle`` constants.
    
    .. attribute:: title
        
        *String*. The text on the button. Equivalent to ``[self title]``.
    
    .. attribute:: action
    
        :class:`Action`. The action that is performed on click. Equivalent to ``[self setTarget:]``
        and ``[self setAction:]``.
    
    .. attribute:: font
        
        :class:`Font`. The font of the button. Equivalent to ``[self font]``.
    
    .. attribute:: state
        
        :ref:`Cocoa constant <literal-consts>`. Equivalent to ``[self state]``.
    
    .. attribute:: keyEquivalent
    
        String. Equivalent to ``[self keyEquivalent]``. If you use escaped strings (such as ``\E``
        for escape or ``\r`` for return), escape the backslashes. Therefore, setting a button
        keyEquivalent to escape is done with ``button.keyEquivalent = "\\E"``.

    
Checkbox
--------

Checkbox is a subclass of :class:`Button`, behaves the same way and adds no method or attributes.
The only differences is that it sets the button ``buttonType`` to ``NSSwitchButton`` and tweaks
the margins to fit XCode's behavior.

.. class:: Checkbox(parent, title)
    
    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param title: A string. See :attr:`Button.title`.
