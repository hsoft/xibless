TabView
=======

The ``TabView`` is a :class:`View` subclass which represents Cocoa's ``NSTabView``. The way it works
is that you add tab items to it with :meth:`TabView.addTab`, which will return a
:class:`TabViewItem`. This tab item has a :attr:`TabViewItem.view` attribute that you can use as a
parent for the subviews you want to add with that tab. Of course, like with any subview, the layout
process in tab views are made independently of the layout in the tab view's parent. Example::

    tabview = TabView(mywindow)
    tab = tabview.addTab("mytab")
    label = Label(mytab.view, "label in my tab")
    
    tabview.packToCorner(Pack.UpperLeft)
    tabview.fill(Pack.Right)
    tabview.fill(Pack.Below)
    tabview.setAnchor(Pack.UpperLeft, growX=True, growY=True)
    label.packToCorner(Pack.UpperLeft)
    label.fill(Pack.Right)

.. class:: TabView(parent)
    
    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    
    .. method:: addTab(label[, identifier=None])
        
        :param label: String. See :attr:`TabViewItem.label`.
        :param identifier: String. See :attr:`TabViewItem.identifier`.
        
        Creates a :class:`TabViewItem` and adds it to self. The created item is returned by the
        method.
    
TabViewItem
-----------

The ``TabViewItem`` is created by :meth:`TabView.addTab` and represents a ``NSTabViewItem``. You
shouldn't create it directly, but you can set it's attributes (except :attr:`TabViewItem.view` which
is read-only).

.. class:: TabViewItem(tabview, label[, identifier=None])
    
    :param tabview: The parent :class:`TabView`.
    :param label: String. See :attr:`TabViewItem.label`.
    :param identifier: String. See :attr:`TabViewItem.identifier`.
    
    .. attribute:: label
        
        String. The label of the tab item. Equivalent to ``[self label]``.
    
    .. attribute:: identifier
        
        String. The identifier of the tab item. Equivalent to ``[self identifier]``.
    
    .. attribute:: view
        
        :class:`View`. Read-Only. The view associated with the tab. Use this as a parent to the
        widgets you want to place in the tab.
        
        In Cocoa, it's possible to set your own view with ``[NSTabViewItem setView:]``, but there
        are technical difficulties in ``xibless`` making this impossible for the moment.
