View
====

The ``View`` is a representation of Cocoa's ``NSView``. It isn't meant to be instatiated directly,
but to be subclassed.

.. class:: View(parent, width, height)

    :param parent: A :class:`View` instance. See :attr:`parent`.
    :param width: Numeric. See :attr:`width`.
    :param height: Numeric. See :attr:`height`.

    Every view has a parent, which in Cocoa is called superview. ``x`` and ``y`` are
    usually set by layout methods, so we don't care about them (they're initialized to ``0``).
    However the size of a widget is important to know before starting the layout process, so we
    add them to the constructor. Many subclasses have defaults for their size, so it's not because
    the ``View`` asks for it that every subclass does so.

    .. attribute:: parent

        :class:`View` *instance*. The superview of the view. It can be ``None``. When set, the view
        will automatically be added to its superview upon creation.

    .. attribute:: x

        *Numeric*. The X position of the view. In Cocoa: ``frame.origin.x``.

    .. attribute:: y

        *Numeric*. The y position of the view. In Cocoa: ``frame.origin.y``.

    .. attribute:: width

        *Numeric*. The width of the view. In Cocoa: ``frame.size.width``.

    .. attribute:: height

        *Numeric*. The height of the view. In Cocoa: ``frame.size.height``.
    
    .. attribute:: menu
        
        :class:`Menu`. The contextual menu for the view.

    .. attribute:: delegate
        
        *Instance or accessor*. View's delegate, which has a different role depending on the
        subclass. The value for this attribute can be either another instance, or a reference, such
        as ``owner`` or ``owner.something``.
    
    .. method:: bind(name, target, keyPath[, valueTransformer])
    
        :param name: *String*
        :param target: *Instance or accessor*.
        :param keyPath: *String*.
        
        Binds self's ``name`` attribute to ``target``'s ``keyPath`` attribute. To bind something
        to a User Defaults value, use the global ``defaults`` accessor. For example, if you want
        to bind the font size of a button to a default value, you'd do
        ``button.bind('fontSize', defaults, 'values.ButtonFontSizePref')``
        
        For now, not all binding options are supported, only the ``valueTransformer`` one. The value
        you have to give to that argument is the value transformer's name (the same name you'd give
        to XCode's interface builder).
    
    .. method:: packToCorner(corner[, margin])
        
        :param corner: A :ref:`corner-constants`
        :param margin: Numeric

        Send the view to a specified corner of its super view. It doesn't care if there's already
        something in there, so if you send two views in the same corner, they're going to overlap.
        To place views relatively to each other, use :meth:`packRelativeTo`.
        
        You can override default margins by specifying a ``margin`` argument.

    .. method:: packRelativeTo(other, side[, align, margin])

        :param other: A :class:`View` instance
        :param side: A :ref:`side-constants`
        :param align: A :ref:`side-constants`
        :param margin: Numeric
        
        Sends the view at the side of another view, specified by ``other``. The way the view is
        placed next to the other is specified by ``side`` and ``align``. ``side`` tells at which
        side of ``other`` we want our view to be. For example, if it's ``Pack.Below``, our view is
        going to be placed under ``other``. ``align`` tells how our view, if it's not the same size
        as ``other``, is going to be aligned. If we countinue our "below" example and align our view
        with ``Pack.Right``, our view's right side is going to be aligned with ``other``'s right
        side. As you probably guessed, ``align`` has to be of a different orientation than ``side``.
        It doesn't make any sense to ``side`` at ``Pack.Below`` and ``align`` at ``Pack.Above``.
        
        The ``align`` argument is optional. If it's not supplied, it will default to ``Left`` if
        ``side`` is vertical and ``Middle`` otherwise.
        
        You can override default margins by specifying a ``margin`` argument.
    
    .. method:: fill(side[, margin, goal])
        
        :param side: One of :ref:`side-constants` or :ref:`corner-constants`
        :param margin: Numeric
        :param goal: Numeric
        
        Makes the view grow in a direction specified by ``size`` until it reaches its superview's
        bounds (respecting the margins, of course). The nice thing about ``fill`` is that if you
        used :meth:`packRelativeTo` to pack views at the view's side you're
        trying to fill, these views are going to count in the filling process. For example, if you
        have a button packed at your right and you're filling to the right, the gain in width will
        be decerased by the button's width and margin and the button will be moved to the right to
        accomodate your growth.
        
        Using a corner constant instead of a size one is a shorthand for calling ``fill()`` twice.
        For example, calling ``fill(Pack.LowerRight)`` is the same as calling both
        ``fill(Pack.Below)`` and ``fill(Pack.Right)``.
        
        You can override default margins by specifying a ``margin`` argument.
        
        You can also override the ``goal`` of the filling operation, that is, the point it's trying
        to reach when it enlarges or shrink. Most of the time, you're not going to need it, but for
        complex layouts, you might, mostly for operations like "fill my view exactly at the same
        point at this other view over there".
    
    .. method:: setAnchor(corner[, growX, growY])
        
        :param corner: One of the :ref:`corner-constants`
        :param growX: Boolean
        :param growY: Boolean
        
        Sets the view autoresizing mask. The corner you specify will be the corner the view "stick
        to" when its parent view is resized. If growX and/or growY is ``True``, the view will grow
        or shrink with its parent view.
    
