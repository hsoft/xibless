TextField
=========

The ``Textfield`` is a :class:`View` subclass that represents Cocoa's ``NSTextField``.

.. class:: TextField(parent, text)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param text: String. See :attr:`text`.
    
    .. attribute:: text
        
        A string that represents the text field's text. Equivalent to ``[self stringValue]``.
    
    .. attribute:: font
        
        :class:`Font`. The font of the text field. Equivalent to ``[self font]``.
    
Label
-----

The ``Label`` is a :class:`TextField` subclass that mimics the presentation of the label in XCode,
that is, uneditable, unselectable, borderless and backgroundless.

.. class:: Label(parent, text)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param text: String. See :attr:`TextField.text`.
