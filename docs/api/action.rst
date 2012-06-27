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
