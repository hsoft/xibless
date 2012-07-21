ImageView
=========

The ``ImageView`` is a :class:`View` subclass that represents Cocoa's ``NSImageView``.

.. class:: ImageView(parent, name[, alignment=const.NSImageAlignCenter])
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param name: String. See :attr:`name`
    :param alignment: :ref:`Cocoa constant <literal-consts>`. See :attr:`alignment`
    
    .. attribute:: name
        
        String. The name of the image that will be loaded on initialization. That image is loaded
        with ``[self setImage:[NSImage imageNamed:<name>]]``.
    
    .. attribute:: alignment
    
        :ref:`Cocoa constant <literal-consts>`. Image alignment within the view. Equivalent to
        ``[self imageAlignment]``. Use with ``NSImageAlignment`` constants.
    

