Layouts
=======

Layouts are technically :class:`View` subclasses, but that's a temporary hack and they are not
generated in Objective-C code. All they do is that they make the task of calling layout-related
methods easier. See :doc:`/layout` for more information.

.. class:: HLayout(left, right)
    
    :param left: List of :class:`View` that are packed on the left side of the layout.
    :param right: List of :class:`View` that are packed on the right side of the layout.
    
    Creates a layout representing a horizontal row with views in it left and right sides. Those
    lists together must contain at least 2 views, but one of the sides can be empty. You can use
    normal layout methods on this layouts and views you've put in the left and right side will be
    auto-arranged inside that layout.
    
    When a layout is created, it automatically fills the parent view (by respecting its inner
    margin). It can be resized afterwards.
    
    .. method:: setAnchor(side)
        
        :param side: One of the :ref:`side-constants`. Only vertical ones.
        
        Because the layout is not generated in Objective-C code, it doesn't make sense to set it's
        autoresizing mask (that's what :meth:`View.setAnchor` does). This method doesn't do that.
        What it does is that it sets the anchor of all its subviews at once, the left subviews
        being anchored left, and the right subviews being anchored right.
