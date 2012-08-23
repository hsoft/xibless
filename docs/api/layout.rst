Layouts
=======

Layouts are technically :class:`View` subclasses (well, actually, there's a ``Layout`` class in the
middle, but it's not intended to be directly instantiated), but that's a temporary hack and they
are not generated in Objective-C code. All they do is that they make the task of calling
layout-related methods easier. See :doc:`/layout` for more information.

.. class:: HLayout(subviews[, filler, height, margin, align])
    
    :param subviews: List of :class:`View`
    :param filler: :class:`View` instance
    :param height: Numeric
    :param margin: Numeric
    :param align: Numeric
    
    Creates a layout representing a horizontal row managing ``subviews``. The first element is the
    leftmost one and the rest is going to be placed sequetially to the right. The list of subviews
    can contain at most one ``None`` element. That element represents an empty space filler. Views
    before the ``None`` element will be aligned to the left, and views after the ``None`` element
    will be aligned right. If there are no ``None`` element, everything is aligned to the left.
    
    If you specify a ``filler`` that element will be the one taking up all free space in your
    layout. That filler must, of course, be present in your subviews and you cannot specify one
    while at the same time having a ``None`` element in your subviews. In other words, at most one
    "thing" can eat up free space in your layout at once, either empty space or a filler.
    
    If you don't specify a ``height``, the height of the highest subview will be used. In a layout,
    all subviews that can have their height adjusted will have their height set to the layout's
    height. Instead of automatically determining the layout's height from subviews, you can specify
    a height with the ``height`` argument.
    
    You can specify a ``margin`` argument if you want to force a certain margin between your layout
    elements. If you don't, standard margins will be applied.
    
    When placing views with a height that is smaller than the layout's height, we have to decide
    how to vertically align the view. Will it be sent above, below, in the middle? You decide. If
    you don't middle is the default alignment. Valid values are ``Pack.Above``, ``Pack.Middle``,
    ``Pack.Below``.
    
    .. method:: setAnchor(side)
        
        :param side: One of the :ref:`side-constants`. Only vertical ones.
        
        Because the layout is not generated in Objective-C code, it doesn't make sense to set it's
        autoresizing mask (that's what :meth:`View.setAnchor` does). This method doesn't do that.
        What it does is that it sets the anchor of all its subviews at once, the left subviews
        being anchored left, and the right subviews being anchored right.

.. class:: VLayout(subviews[, filler, width, margin, align])
    
    :param subviews: List of :class:`View`
    :param filler: :class:`View` instance
    :param width: Numeric
    :param margin: Numeric
    :param align: Numeric
    
    The principle of ``VLayout`` is the same as :class:`HLayout`, but vertically. The order in which
    subviews are consider is from top to bottom. The first subview is at the top, and the last is at
    the bottom.
    
    Alignment for vertical layout is done horizontally. Therefore, valid values are ``Pack.Left``,
    ``Pack.Middle``, ``Pack.Right``. Default is left.

.. class:: VHLayout(subviews[, hfillers, vfiller, width, hmargin, vmargin, halign, valign])
    
    :param subviews: List of lists of :class:`View`
    :param hfillers: A collection of :class:`View`
    :param vfiller: A :class:`View` instance.
    :param width: Numeric
    :param hmargin: Numeric
    :param vmargin: Numeric
    :param halign: Numeric
    :param valign: Numeric
    
    This is a shortcut to creating a :class:`VLayout` with multiple :class:`HLayout` inside. The
    ``subview`` argument must be given in a "grid" fashion like this::
    
        VHLayout([
            [line1view1, line1view2],
            [line2view1, line2view2, line2view3],
            [line3view1, line3view2],
        ])
    
    Specifying fillers in such a layout is a complex matter. There's two types of fillers, first
    the horizontal fillers. They're given as a collection of views (because there can be more than
    one in the grid) as the ``hfillers`` argument. You include the filler for each line (if there's
    no filler for a line, you add nothing) of the layout. The order in which they're added is not
    important. If you have space fillers (``None`` fillers), you don't have to add ``None`` to the
    ``hfillers`` collection. For example, if you want the second view of each line to be fillers,
    you'd specifiy ``{line1view2, line2view2, line3view2}`` as the ``hfillers`` argument.
    
    Then, there's also the ``vfiller`` argument, which is the vertical filler (there's only one).
    Because the ``VHLayout`` is a vertical layout that dynamically creates horizontal layouts, it's
    impossible for you to specify a filler instance beforehand because you don't have access to the
    horizontal layout instances that have yet to be created. Therefore, in the case of ``VHLayout``,
    you can specify an instance **in** the view array. For example, if, in the example above, you
    wanted to make the middle line the filler, you could have specified any of ``line2view1``,
    ``line2view2`` or ``line2view3`` as the ``vfiller`` and the result would have been the same.
    
    Margin and align arguments are the same as simple layouts. ``hmargin`` is the horizontal margin
    and ``vmargin`` is the vertical one. ``halign`` is the horizontal alignment (applied to the
    **vertical** layout) and ``valign`` is the vertical alignment (applied to the **horizontal**
    layout).
