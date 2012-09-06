Menu
====

The ``Menu`` is a class that represents Cocoa's ``NSMenu``.

.. class:: Menu(name)

    :param name: String. See :attr:`name`
    
    Creates a menu with the specified name.
    
    .. attribute:: name
    
        The name of the menu.
    
    .. method:: add(menu_or_item[, index=None])
    
        :param menu_or_item: :class:`Menu` or :class:`MenuItem`.
        :param index: Integer.
        
        Adds the instance specified by ``menu_or_item`` to its subitems. If ``index`` is not
        ``None``, the item will be inserted at the specified index. Otherwise, it will be added at
        the end of the list.
    
    .. method:: addItem(name[, action=None, shortcut=None, tag=None, index=None])
    
        :param name: String. See :attr:`MenuItem.name`.
        :param action: :class:`Action`. See :attr:`MenuItem.action`.
        :param shortcut: String. See :attr:`MenuItem.shortcut`.
        :param tag: Integer or :ref:`literal-consts`. See :attr:`MenuItem.tag`.
        :param index: Integer. See :meth:`add`.
        
        Creates a :class:`MenuItem` and adds it to the menu's items. The method arguments are
        passed to the menu item constructor.
    
    .. method:: addSeparator([index=None])
    
        :param index: Integer. See :meth:`add`.
        
        Add a separator item to the menu.
    
    .. method:: addMenu(name[, index=None])
        
        :param name: String. See :attr:`name`.
        :param index: Integer. See :meth:`add`.
        
        Create a new submenu and add it to our menu's items.
    
    .. method:: removeItem(index)
        
        :param index: Integer.
        
        Remove item at ``index``.
    
MenuItem
--------

The ``MenuItem`` is a class that represents Cocoa's ``NSMenuItem``.

.. class:: MenuItem(name, action=None, shortcut=None, tag=None)
    
    :param name: String. See :attr:`MenuItem.name`.
    :param action: :class:`Action`. See :attr:`MenuItem.action`.
    :param shortcut: String. See :attr:`MenuItem.shortcut`.
    :param tag: Integer or :ref:`literal-consts`. See :attr:`MenuItem.tag`.
    
    .. attribute:: name
        
        The name of the menu.
    
    .. attribute:: action
        
        :class:`Action`. The action that is performed on click. Equivalent to ``[self setTarget:]``
        and ``[self setAction:]``.
    
    .. attribute:: shortcut
        
        A string that represent the keyboard shortcut that triggers the item. This string has the
        format "modifiers+letter", for example, "cmd+f". Available modifiers are "cmd", "ctrl",
        "alt" and "shift".
        
        Some special characters are supported through special identifiers. The list of supported
        identifiers is :ref:`there <shortcut-key-consts>`. For example, if you want a shortcut that
        is activated on cmd+<up arrow>, your shorcut would be ``cmd+arrowup``.
    
    .. attribute:: tag
        
        Integer value corresponding to ``[self tag]``.
    
    .. attribute:: state
        
        :ref:`Cocoa constant <literal-consts>`. Use with ``NSCellStateValue`` constants.
    

MainMenu
--------

This special class builds the same main menu that is created when you create a new XIB project.

.. class:: MainMenu(appname)
    
    :param appname: String
    
    The ``appname`` param is used to create menu items like "Quit <appname>" and "About <appname>".
