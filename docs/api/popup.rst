Popup
=====

The ``Popup`` is a :class:`Control` subclass which represents Cocoa's ``NSPopUpButton``.

.. class:: Popup(parent[, items=None])

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param items: A list of strings.
    
    If the ``items`` argument is not ``None``, the strings in that list will be added to the popup's
    :attr:`menu`.

    .. attribute:: menu
        
        :class:`Menu`. The menu that pops up when you click on the popup. You can manimulate that
        menu like you manipulate a normal menu (it's in fact, a normal menu).
    
    .. attribute:: pullsdown
    
        **Boolean**. Tells whether the poopup is of "Pull Down" style. Equivalent to
        ``[self pullsDown]``.
