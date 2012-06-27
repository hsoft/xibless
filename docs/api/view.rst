View
====

The ``View`` is a representation of Cocoa's ``NSView``. It isn't meant to be instatiated directly,
but to be subclassed.

.. class:: View(parent, width, height)

    The ``View`` isn't mean't to be instatiated directly, but every subclass still has to call this
    contructor. Every view has a parent, which in Cocoa is called superview. ``x`` and ``y`` are
    usually set by layout methods, so we don't care about them (they're initialized to ``0``).
    However the size of a widget is important to know before starting the layout process, so we
    add them to the constructor. Many subclasses have defaults for their size, so it's not because
    the ``View`` asks for it that every subclass does so.

    .. attribute:: parent

        :class:`View` *instance*. The superview of the view. It can be ``None``. When set, the view
        will automatically be added to its superview upon creation.

    .. attribute:: x

        *Numeric*. The X position of the view. Equivalent to ``[self frame].origin.x]``.

    .. attribute:: y

        *Numeric*. The y position of the view. Equivalent to ``[self frame].origin.y]``.

    .. attribute:: width

        *Numeric*. The width of the view. Equivalent to ``[self frame].size.width]``.

    .. attribute:: height

        *Numeric*. The height of the view. Equivalent to ``[self frame].size.height]``.

    .. method:: packToCorner(corner)

        Send the view to a specified corner of its super view. ``corner`` is one of the
        :ref:`corner-constants`. It doesn't care if there's already something in there, so if you
        send two views in the same corner, they're going to overlap. To place views relatively to
        each other, use :meth:`packRelativeTo`

    .. method:: packRelativeTo(other, side, align)

        Sends the view at the side of another view, specified by ``other``. The way the view is
        placed next to the other is specified by ``side`` and ``align``, which are both
        :ref:`side-constants`. ``side`` tells at which side of ``other`` we want our view to be.
        For example, if it's ``Pack.Below``, our view is going to be placed under ``other``.
        ``align`` tells how our view, if it's not the same size as ``other``, is going to be
        aligned. If we countinue our "below" example and align our view with ``Pack.Right``, our
        view's right side is going to be aligned with ``other``'s right side. As you probably
        guessed, ``align`` has to be of a different orientation than ``side``. It doesn't make any
        sense to ``side`` at ``Pack.Below`` and ``align`` at ``Pack.Above``.
    
    .. method:: fill(side)
        
        Makes the view grow in a direction specified by ``size`` (a :ref:`side-constants`) until
        it reaches its superview's bounds (respecting the margins, of course). The nice thing about
        ``fill`` is that if you used :meth:`packRelativeTo` to pack views at the view's side you're
        trying to fill, these views are going to count in the filling process. For example, if you
        have a button packed at your right and you're filling to the right, the gain in width will
        be decerased by the button's width and margin and the button will be moved to the right to
        accomodate your growth.

.. _corner-constants:

Corner constants
----------------

.. data:: Pack.UpperLeft
.. data:: Pack.UpperRight
.. data:: Pack.LowerLeft
.. data:: Pack.LowerRight

.. _side-constants:

Side constants
----------------

.. data:: Pack.Left
.. data:: Pack.Right
.. data:: Pack.Above
.. data:: Pack.Below
