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
    
    .. attribute:: arrowPosition
        
        :ref:`Cocoa constant <literal-consts>`. The arrow position (center, bottom or none) in the
        pop up. In Cocoa, it's ``cell.arrowPosition``. Use with ``NSPopUpArrowPosition`` constants.

Creating an "Action" popup
--------------------------

Many apps have an "Action" menu, a pop up menu with the little "gears" icon that gives access to a
menu with different actions to perform. There's a couple of things to keep in mind when you
construct these menus:

1. The menu has to be of ``pulldown`` type.
2. The gears image is built in and its name is "NSActionTemplate".
3. The first item of the menu, which has to be hidden, is used to determine the image displayed in
   the popup.
4. In OS X versions prior to 10.7, your popup arrow will be at the wrong place unless you set
   ``arrowPosition`` to ``NSPopUpArrowAtBottom``.

Anyway, here's an example you can use::

    actionPopup = Popup(window)
    actionPopup.pullsdown = True
    actionPopup.bezelStyle = const.NSTexturedRoundedBezelStyle
    actionPopup.arrowPosition = const.NSPopUpArrowAtBottom
    firstItem = actionPopup.menu.addItem("")
    firstItem.hidden = True
    firstItem.image = 'NSActionTemplate'
    actionPopup.menu.addItem("Action 1")
    actionPopup.menu.addItem("Action 2")
    actionPopup.menu.addItem("Action 3")
