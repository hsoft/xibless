TextView
========

The ``TextView`` is a :class:`View` subclass that represents Cocoa's ``NSTextView``.

.. class:: TextView(parent)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    
    .. attribute:: text
        
        A string that represents the text field's text. Equivalent to
        ``[[[self textStorage] mutableString] string]``.
    
    .. attribute:: font
        
        :class:`Font`. The font of the text field. Equivalent to ``[[self textStorage] font]``.
    
