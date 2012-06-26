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

The command line ``xibless`` command also has a ``run`` command letting you quicky see what your
script looks like as a real UI. If you run::

    xibless run <source>

the source script will be compiled and wrapped around a "RunUI" app which will simply display the
window.

Now, all this does is that it generates UI code. ``xibless`` hasn't, yet, any integrated solution
to let you easily build a XCode-less program. However, what you can do is to look at the ``demos``
folder and base yourself on those demos (which are completely XCode-less) to build your own project.
