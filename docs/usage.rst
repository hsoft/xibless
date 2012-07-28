=====
Usage
=====

``xibless`` can be used either from the command line or through Python. To use it from the command
line, you type::

    xibless compile <source> <dest>

``source`` is the path of the Python module you wrote that describes the UI you want to build.
``dest`` is the path you want your resulting Objective-C file to be written at. To use ``xibless``
directly from Python, the usage is similar::

    import xibless
    xibless.generate(source, dest)

These commands will generate code at ``dest``. If ``dest`` has an extension other than ``.h``, a
``.h`` header will be generated alongside it. If ``dest`` doesn't have an extension, a ``.m``
extension is automatically appended.

The command line ``xibless`` command also has a ``run`` command letting you quicky see what your
script looks like as a real UI. If you run::

    xibless run <source>

the source script will be compiled and wrapped around a "RunUI" app which will simply display the
window.

Now, all this does is that it generates UI code. ``xibless`` hasn't, yet, any integrated solution
to let you easily build a XCode-less program. However, what you can do is to look at the ``demos``
folder and base yourself on those demos (which are completely XCode-less) to build your own project.

Enabling Localization
---------------------

``xibless.generate()`` has a ``localizationTable`` argument (``--loc-table`` from the command line).
If you set it to a non-empty string, string localization will be enabled, that is, all strings will
be wrapper around ``NSLocalizedStringFromTable(theString, localizationTable, @"")``. This enables
you to have localized UIs. See an example of such UI in the ``localized`` demo.

Arbitrary script arguments
--------------------------

When calling ``generate()`` from Python, you can pass arbitrary arguments through ``args``. What you
pass will be available as the ``args`` global value in the script. For example, if you generate a UI
with::

    xibless.generate(source, dest, args={'foo': 'bar'})

You can do stuff like this in your script::

    myLabel = Label(window, text=args['foo'])

If not specified, ``args`` in the script will be an empty dictionary.
