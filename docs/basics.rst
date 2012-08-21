=================
UI Scripts Basics
=================

A ``xibless`` UI script is a Python script that describes a UI to build through Objective-C code
that ``xibless`` is going to generate from that script. It creates objects like :class:`Window` or
:class:`Button`, sets their properties and place them in their superview.

When a UI script is generated, it creates an Objective-C unit with one function that takes one
argument, the "File Owner", and returns the script's ``result`` (see next section). Here's an
example of what its signature might look like:

.. code-block:: objective-c

    NSWindow* createMainWindow(AppDelegate *owner);

Namespace and special variables
-------------------------------

Every class described in the :doc:`api/index` section are directly in the script namespace. Therefore,
if you want to create a :class:`Label`, you do it thus::

    label = Label(parent, text="hello!")

Other than class references, there's also a few special variables to keep in mind.

1. ``result``. This is where you must assign the main "result" of the script, most of the time a
   main menu or a window. All you have to do to assign it is to do so in the module's global
   namespace.

.. code-block:: python

   result = Window(400, 200, title="My Window")

2. ``owner``. This is a bit like a XIB's "File's owner". You can reference to it when setting
   properties and you can also set its own properties. Of course, the owner has to actually have
   the property you're trying to set on it, otherwise, you'll have a compilation error.

.. code-block:: python

    button.action = Action(target=owner, selector='myAction:')
    owner.mySuperButton = button

3. ``NSApp``. A bit like ``owner`` except it references Cocoa's ``NSApp``.

.. code-block:: python

    menu.addItem("Quit", action=Action(NSApp, 'terminate:'), shortcut='cmd+q')

4. ``ownerclass``. If you want to send an ``owner``, you have to set the ``ownerclass`` variable
   in your script to the name of the class the owner is going to be. If you do that, you also have
   to set ``ownerimport`` to the name of the unit to import to have ``ownerclass`` definition.

.. code-block:: python
    
    ownerimport = 'AppDelegate.h'
    ownerclass = 'AppDelegate'

5. ``const``. See :ref:`literal-consts` below.

6. ``defaults``. A reference to ``[NSUserDefaultsController sharedUserDefaultsController]``. For
   now, it's only useful when you call :meth:`View.bind`.

.. _literal-consts:

Literal Constants
-----------------

Some widget attributes require literal constants from the Cocoa framework. For example,
``NSButton.state`` is either ``NSOnState``, ``NSOffState`` or ``NSMixedState``. You can't use
strings to set these values because they will be wrapped around ``@""`` during code generation. When
you need these types of values, use the ``const`` identifier which is present in the UI script
namespace. For example::

    findMenu.addItem("Find...", Action(None, 'performFindPanelAction:'), 'cmd+f', tag=const.NSFindPanelActionShowFindPanel)

The API documentation will indicate when such a constant is required. Ideally, there will be a
constant in ``xibless`` (see :doc:`api/const`) wrapping every Cocoa constant, but doing so is boring
work and I'm often too excited doing not-boring work to spend time wrapping constants. But
eventually...

**Bitwise OR-ed flags**. Some attributes are actually masks, which required bitwise-OR-ed values.
Well, you can do that in ``xibless``. Use the ``|`` char as in ``const.flag1 | const.flag2``.

Memory Management
-----------------

Everything created inside a UI script is auto-released, which means that you have to retain it when
you store the result and in your owner's properties set by the script.

Of course, if an object is "naturally" retained by another object created in the script, such as
a ``NSMenuItem`` added to a ``Menu`` or a view added to a superview, then you don't have to manually
retain those objects.

Unsupported Properties
----------------------

``xibless`` being in early development, it doesn't support everything Cocoa has to offer yet. If you
find yourself in a situation where an attribute you want to set on an instance isn't supported,
you can always try to set it in its ``properties`` dictionary, for example with::

    foo.properties['delegate'] = bar

It's not guaranteed to work, but it very well might.

Custom subclasses
-----------------

In XCode's interface builder, it's possible to specify a custom class to instantiate instead of the
base class. For example, if you have a home grown ``NSTableView`` subclass and want to instantiate
it in an XIB, you'd change the table view's class name to ``MyTableView``. In ``xibless``, you can
do the same by setting the ``OBJC_CLASS`` attribute in this fashion::

    table = TableView(window)
    table.OBJC_CLASS = 'MyTableView'

Of course, as is the case with XIB's your custom class will be instantiated with the same arguments
as a typical ``NSTableView`` would.

Import from modules
-------------------

Because UI scripts are Python modules, it's possible to import from other modules. The folder in
which the UI script is will be in ``PYTHONPATH``, so you can do stuff like add a ``common.py`` unit
and then do ``from common import MyLabelSubclass`` in your UI scripts.

The only thing to remember, however, is that the magic that goes on in UI scripts to put all xibless
classes in your UI script's global namespace doesn't work for imported modules. Therefore, if your
module use any xibless classes, you have to import them yourself from the ``xibless`` package (and
you'll have to figure out where they live in the package). That's far from ideal, I'll fix that
some day.
