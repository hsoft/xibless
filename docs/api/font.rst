Font
====

``Font`` represents Cocoa's ``NSFont`` and is used as values for ``font`` attributes in views that
have it.

.. class:: Font(family, size[, traits=None])
    
    :param family: A :ref:`font-family` or a string.
    :param size: A :ref:`font-size` or a number.
    :param traits: A list of :ref:`font-trait`.
    
    Creates a font with the specified family, size and traits. ``family`` can be one of the
    constants or directly a font family name. Same thing for size. The traits is a list of
    constants (example: ``[FontTrait.Bold, FontTrait.Italic]``).

.. _font-family:

Font Family constants
---------------------

These represent their ``NSFont`` constructor counterparts. For example, a font with
``FontFamily.Label`` will be created as ``[NSFont labelFontOfSize:<size>]``

.. data:: FontFamily.System
.. data:: FontFamily.Label
.. data:: FontFamily.Menu
.. data:: FontFamily.Menubar
.. data:: FontFamily.Message
.. data:: FontFamily.Palette
.. data:: FontFamily.Titlebar
.. data:: FontFamily.Tooltips

.. _font-size:

Font Size constants
-------------------

The first 3 constants are translated to their corresponding ``NSFont`` class methods (for example,
``[NSFont systemFontSize]``) and the last 3 are translated to
``[NSFont systemFontSizeForControlSize:<const>]`` (for example, 
``[NSFont systemFontSizeForControlSize:NSRegularControlSize]``).

.. data:: FontSize.System
.. data:: FontSize.SmallSystem
.. data:: FontSize.Label
.. data:: FontSize.RegularControl
.. data:: FontSize.SmallControl
.. data:: FontSize.MiniControl

.. _font-trait:

Font Trait constants
--------------------

.. data:: FontTrait.Bold
.. data:: FontTrait.Italic
