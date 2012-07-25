Toolbar
=======

Represents a ``NSToolbar``. You shouldn't instantiate it directly, alsways instatiate it through
:meth:`Window.createToolbar`.

**NSToolbar, delegate and XIBs**. I don't know how XCode manages to allow the design of toolbars
without using the delegate property of that toolbar. My guess is that they use some kind of private
API. To create a functional toolbar, one has to have a toolbar delegate to create ``NSToolbarItem``
instance. This is what ``xibless`` does. Therefore, consider your toolbar's delegate slot taken.

Moreover, that delegate has to be allocated and created at some point, but there is no convenient
way to pass the reference's responsibility to the ``xibless`` user. Therefore, the instance of the
delegate created for the toolbar will be **leaked**, so will toolbar items.

In most cases, this isn't a big deal because the window that contains a toolbar is often a window
that lives as long as the application. However, if the leak of the toolbar delegate is a problem,
what you should do is to take the ownership of the delegate in your own code and release it
yourself.

.. class:: Toolbar
    
    .. attribute:: displayMode
        
        :ref:`Cocoa constant <literal-consts>`. Whether the toolbar displays images and text, or
        just images, or just text. Use with ``NSToolbarDisplayMode`` constants.
    
    .. attribute:: allowsUserCustomization
    
        Boolean. Whether the user can customize the toolbar.
    
    .. attribute:: autosavesConfiguration
        
        Boolean. Whether the toolbar's state is autosaved/restored.
    
    .. method:: addItem(identifier, label[, image])
        
        :param identifier: String
        :param label: String
        :param image: String
        
        Creates a :class:`ToolbarItem` with the specified arguments, adds it to the toolbar and
        returns it. Note that to avoid needless verbosity, the final identifier of the item will
        be the concatenation of the toolbar's identifier and the argument. So if your toolbar's
        identifier is ``foo`` and you call ``additem('bar', 'mylabel')``, the item's identifier
        will be ``foobar``.
    
    .. attribute defaultItems
        
        A list of item identifiers that are in the default toolbar configuration. This attribute
        isn't automatically populated, so to *have* to set it to have a functional toolbar.
    
    .. method:: flexibleSpace()
    .. method:: space()
    .. method:: separator()
        
        Return a :ref:`Cocoa constant <literal-consts>` representing one of the built-in toolbar
        items. Use it to populate :attr:`defaultItems`.
    
.. class:: ToolbarItem
    
    .. attribute:: identifier
        
        String. The identifier of the item.
    
    .. attribute:: label
        
        String. The label of the item.
    
    .. attribute:: paletteLabel
        
        String. The label of the item in the configuration palette. Unless you change it, it will
        be the same value as :attr:`label`
    
    .. attribute:: image
        
        String. Name of the image to be used for the item.
    
    .. attribute:: view
        
        :class:`View`. View associated with the item (if set, it replaces the :attr:`image`).
    
    .. attribute:: minSize
    
        :class:`Size`. Minimum size of the :attr:`view`. Unless you change it, will be set to the
        view's size.
    
    .. attribute:: maxSize
    
        :class:`Size`. Maximum size of the :attr:`view`. Unless you change it, will be set to the
        view's size.
    
