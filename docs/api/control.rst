Control
=======

The ``Control`` is a :class:`View` subclass which represents Cocoa's ``NSControl``.

.. class:: Control(parent, width, height)

    :param parent: A :class:`View` instance. Same as :attr:`View.parent`.
    :param width: Numeric. See :attr:`View.width`.
    :param height: Numeric. See :attr:`View.height`.
    
    .. attribute:: font
        
        :class:`Font`. The font of the control. Equivalent to ``[self font]``.
    
    .. attribute:: controlSize
        
        :ref:`Cocoa constant <literal-consts>`. One of the 3 Regular, Small and Mini pre-defined
        control size. Setting this attribute will change the font size and height of the control
        to pre-defined values (like Interface Bulder does). Use with ``NSControlSize`` constants.
    
    .. attribute:: action
    
        :class:`Action`. The action that is performed on click. Equivalent to ``[self setTarget:]``
        and ``[self setAction:]``.
    

Action
======

The ``Action`` class doesn't wrap any particular Cocoa class, but is a structure that is used as
an argument of widgets' ``action`` attribute.

.. class:: Action(target, selector)
    
    The ``target`` argument is the same as Cocoa's ``setTarget:``. It can be the ``owner``,
    ``NSApp``, any other object reference. If you want to mimic XIB's "First Responder", set the
    ``target`` to ``None``.
    
    The ``selector`` argument is the selector name, which is a simple string. For example,
    ``"fooAction:"`` is the equivalent of ``@selector(fooAction:)``.
