SplitView
=========

The `SplitView` wraps Cocoa's ``NSSplitView``. When you instantiate it, you tell it how many
subviews it has, and then populate those subviews. Example::

    split = SplitView(window, 3, vertical=True)
    label1 = Label(split.subviews[0], "First Split")
    label2 = Label(split.subviews[1], "Second Split")
    label3 = Label(split.subviews[2], "Third Split")

.. class:: SplitView(parent, splitCount, vertical)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param splitCount: Numeric. How many subviews the split has. See :attr:`subviews`.
    :param vertical: Boolean. See :attr:`vertical`.
    
    .. attribute:: vertical
    
        Boolean. Whether the split dividers are vertical. Equivalent to ``[self isVertical]``.
    
    .. attribute:: subviews
        
        A list of :class:`View` created on the split's initialization. Those views are populated in
        a manner similar to what you do with subviews in :class:`TabView`.
    
