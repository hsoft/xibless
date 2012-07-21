Base Types
==========

Many attributes require more than strings, numbers, booleans or instance of other classes. So here
they are.

Size
----

.. class:: Size(width, height)
    
    Wraps ``NSSize``.

Rect
----

.. class:: Rect(x, y, width, height)
    
    Wraps ``NSRect``.

Color
-----

.. class:: Color(red, green, blue[, alpha=1.0])
    
    Wraps ``NSColor``. Creates an initialized a color instance with the supplied RGBA values.

Font
----

.. class:: Font(family, size[, traits=None])
    
    :param family: A :ref:`font-family` or a string.
    :param size: A :ref:`font-size` or a number.
    :param traits: A list of :ref:`font-trait`.
    
    Wraps ``NSFont``. Creates a font with the specified family, size and traits. ``family`` can be
    one of the constants or directly a font family name. Same thing for size. The traits is a list
    of constants (example: ``[FontTrait.Bold, FontTrait.Italic]``).

Action
------

.. class:: Action(target, selector)

    The ``Action`` class doesn't wrap any particular Cocoa class, but is a structure that is used as
    an argument of widgets' ``action`` attribute.
    
    The ``target`` argument is the same as Cocoa's ``setTarget:``. It can be the ``owner``,
    ``NSApp``, any other object reference. If you want to mimic XIB's "First Responder", set the
    ``target`` to ``None``.
    
    The ``selector`` argument is the selector name, which is a simple string. For example,
    ``"fooAction:"`` is the equivalent of ``@selector(fooAction:)``.