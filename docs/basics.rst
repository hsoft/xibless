=================
UI Scripts Basics
=================

A ``xibless`` UI script is a Python script that describes a UI to build through Objective-C code
that ``xibless`` is going to generate from that script. It creates objects like :ref:`Window` or
:ref:`Button`, sets their properties and place them in their superview.

When a UI script is generated, it creates an Objective-C unit with one function that takes one
argument, the "File Owner", and returns the script's ``result`` (see next section). Here's an
example of what its signature might look like:

.. code-block:: objective-c

    NSWindow* createMainWindow(AppDelegate *owner);

Namespace and special variables
-------------------------------

Every class described in the :doc:`api` section are directly in the script namespace. Therefore,
if you want to create a :ref:`Label`, you do it thus::

    label = Label(parent, text="hello!")

Other than class references, there's also a few special variables to keep in mind.

1. ``result``. This is where you must assign the main "result" of the script, most of the time a
   main menu or a window. All you have to do to assign it is to do so in the module's global
   namespace.

.. code-block:: python

   result = Window(300, 300, 400, 200, title="My Window")

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
   in your script to the name of the class the owner is going to be.

.. code-block:: python
    
    ownerclass = 'AppDelegate'

5. ``const``. This identifier is used when you want to set a property to one of Cocoa's constants,
   such as ``NSOnState``. Don't use strings for such values because during code generation, they'll
   be wrapper in ``@""``.

.. code-block:: python

    findMenu.addItem("Find...", Action(None, 'performFindPanelAction:'), 'cmd+f', tag=const.NSFindPanelActionShowFindPanel)

Memory Management
-----------------

At this moment, there's no memory management and there's tons or memory leaks eveywhere, but in the
future, everything created inside a UI script will be auto-released, which means that you'll have to
retain it when you store the result and in your owner's properties set by the script.

Of course, if an object is "naturally" retained by another object created in the script, such as
a ``NSMenuItem`` added to a ``Menu`` or a view added to a superview, then you don't have to manually
retain those objects.
