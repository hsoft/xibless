======
Layout
======

All :class:`View` subclasses in ``xibless`` have :attr:`~View.x`, :attr:`~View.y`, :attr:`~View.width`
and :attr:`~View.height` properties. Technically, you could place all your views by manually setting
all those properties, but that would become a pain pretty fast. ``xibless`` has methods to help
place your widgets.

The first thing to know about the current layout helpers is that they're not set into stone and are
likely going to change. I eventually want to support the layout feature introduced in OS X 10.7
and that is probably going to require big changes in the layout methods.

The second thing to keep in mind before doing layouts is that your widgets are expected to have their
size set before you start the layout process. If you put a button next to a text field and then
make the text field grow, there's no mechanism (yet) that will correctly detect that and make the
button follow (except if you use :meth:`View.fill`)

A third thing to know is that ``xibless`` tries to mimic margins in Interface Builder. So when we
send a widget in a corner, we take the margin into account. For now, it's not possible to override
those margins.

The way layouts work in ``xibless`` is by "packing". You start with an empty superview, add some
widgets to it and start doing the layout by sending one of your widgets in one of the corners,
usually the upper left corner. Then, you take another widget and send it next or below the widget
you've just placed, and so on, until you've packed all your widgets.

The first part of the process, sending a widget to a corner of its superview, is done with
:meth:`View.packToCorner`. You call it by giving it a corner as an argument. For example::

    button.packToCorner(Pack.UpperLeft)

sends ``button`` to the upper left corner of its superview.

The second part, packing widgets relative to each other, is done through :meth:`View.packRelativeTo`.
This method takes an ``other`` argument, which is the widget to place our target next to, ``side``
which is the side of ``other`` at which to place our target, and then ``align``, which is the side
to align to if your target widget is smaller than ``other``. For example::

    button.packRelativeTo(textfield, side=Pack.Below, align=Pack.Right)

will place ``button`` below ``textfield``. If the button's width is smaller than the textfield's,
the button upper right corner of the button will be aligned with the textfield's lower right corner.
If ``align`` was set to ``Pack.Left``, the button's upper left corner would have been aligned with
the textfield's lower left corner.

Now, there's also :meth:`View.fill`. This tells a widget to adjust its width or height so that it
takes all available space in a direction. For example::

    textfield.fill(Pack.Right)

increases textfield's width until it reaches the superview's bounds. The cool thing about ``fill``
is that if you used ``packRelativeTo`` to put another widget next to it, it will consider that
widget in the filling calculations. So, for example, if you put a button at the right of that
textfield and then call ``fill``, the amount by which the textfield grows will be reduced by the
width (and margin) of the button. The button will even be moved to the right accordingly.

Finally, there's :meth:`View.setAnchor` that sets the "resizing mask" property (you know, the little
red bars around and inside a square we toggle in Interface Builder to determine what side the widget
will follow when its superview is resized). This property works like the one in Interface Builder
because... it's the same! For example, if you want your textfield to grow horizontally and be
anchored to the upper left corner, you call::

    textfield.setAnchor(Pack.UpperLeft, growX=True)
