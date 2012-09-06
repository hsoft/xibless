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
    
    .. attribute:: dividerStyle
    
        :ref:`Cocoa constant <literal-consts>`. Style of the dividers. Use
        ``NSSplitViewDividerStyle`` constants.
    
    .. attribute:: subviews
        
        A list of :class:`View` created on the split's initialization. Those views are populated in
        a manner similar to what you do with subviews in :class:`TabView`.
    

Direct view hierarchy in split views
------------------------------------

If you create a split view in a way similar to the example above, you'll have a split view populated
by plain ``NSView`` instances which will then be the parent the views you're going to put in them.
Sometimes (and even often), you rather want to put your view directly in the split view. In these
cases, set the initial ``splitCount`` to ``0`` and create your views with the split directly as a
parent, like this::

    split = SplitView(window, 0, vertical=True)
    label1 = Label(split, "First Split")
    label2 = Label(split, "Second Split")
    label3 = Label(split, "Third Split")

The order in which you create your subviews will then be very important because it will determine
the order of the views in the split.
