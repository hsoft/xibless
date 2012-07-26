Popup
=====

The ``Popup`` is a :class:`Button` subclass which represents Cocoa's ``NSPopUpButton``.

.. class:: Popup(parent[, items=None])

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param items: A list of strings.
    
    If the ``items`` argument is not ``None``, the strings in that list will be added to the popup's
    :attr:`menu`.

    .. attribute:: menu
        
        :class:`Menu`. Although this is a :class:`View` attribute (for context menus), it has a
        special role in the ``Popup`` because it's the menu that pops up when you click on it. The
        difference with the View's attribute is that you don't have to create a Menu instance
        yourself, it's already automatically created for you.
    
    .. attribute:: pullsdown
    
        **Boolean**. Tells whether the poopup is of "Pull Down" style. Equivalent to
        ``[self pullsDown]``.
