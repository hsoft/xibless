Button
======

The ``Button`` is a :class:`Control` subclass which represents Cocoa's ``NSButton``.

.. class:: Button(parent, title[, action=None])

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param title: A string. See :attr:`title`.
    :param action: An :class:`Action`. See :attr:`Control.action`.
    
    .. attribute:: buttonType
    
        :ref:`Cocoa constant <literal-consts>`. The type of the button. Equivalent to
        ``[self buttonType]``. Use with ``NSButtonType`` constants.
    
    .. attribute:: bezelStyle
    
        :ref:`Cocoa constant <literal-consts>`. The style of the button. Equivalent to
        ``[self bezelStyle]``. Use with ``NSBezelStyle`` constants.
    
    .. attribute:: bordered
    
        *Boolean*. Whether the button has a border.
    
    .. attribute:: title
        
        *String*. The text on the button. Equivalent to ``[self title]``.
    
    .. attribute:: font
        
        :class:`Font`. The font of the button. Equivalent to ``[self font]``.
    
    .. attribute:: state
        
        :ref:`Cocoa constant <literal-consts>`. Use with ``NSCellStateValue`` constants.
    
    .. attribute:: shortcut
        
        A string that represent the keyboard shortcut that triggers the button. This string has the
        format "modifiers+letter", for example, "cmd+f". Available modifiers are "cmd", "ctrl",
        "alt" and "shift".
        
        Some special characters are supported through special identifiers. The list of supported
        identifiers is :ref:`there <shortcut-key-consts>`. For example, if you want a shortcut that
        is activated on cmd+<up arrow>, your shorcut would be ``cmd+arrowup``.
    
    .. attribute:: image
        
        *String*. The name of an image for the button. Equivalent to ``[self image]``.
    
    .. attribute:: imagePosition
        
        :ref:`Cocoa constant <literal-consts>`. Equivalent to ``[self imagePosition]``.
        Use with ``NSCellImagePosition`` constants.


Buttons and Layouts
-------------------

If you fire up Interface Builder and try to play with a button bezel style, you'll notice that
changing it changes many more things too, such as the layouts and the fonts. ``xibless`` does it
too (it tries to do exactly as IB does). Whenever :attr:`Button.bezelStyle` is changed, layout
delta values and fonts are changed. Therefore, if you should always change the :attr:`Button.font`
and/or do the layouts *after* you've changed your bezel style.
    
Checkbox
--------

Checkbox is a subclass of :class:`Button`, behaves the same way and adds no method or attributes.
The only differences is that it sets the button ``buttonType`` to ``NSSwitchButton`` and tweaks
the margins to fit XCode's behavior.

.. class:: Checkbox(parent, title)
    
    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param title: A string. See :attr:`Button.title`.
