Constants
=========

These are the constants used throughout ``xibless``.

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

.. _corner-constants:

Corner constants
----------------

.. data:: Pack.UpperLeft
.. data:: Pack.UpperRight
.. data:: Pack.LowerLeft
.. data:: Pack.LowerRight

.. _side-constants:

Side constants
----------------

.. data:: Pack.Left
.. data:: Pack.Right
.. data:: Pack.Above
.. data:: Pack.Below

.. _panel-style-constants:

PanelStyle constants
--------------------

.. data:: PanelStyle.Regular
.. data:: PanelStyle.Utility
.. data:: PanelStyle.HUD

.. _text-alignment-constants:

TextAlignment constants
-----------------------

.. data:: TextAlignment.Left
.. data:: TextAlignment.Right
.. data:: TextAlignment.Center
.. data:: TextAlignment.Justified
.. data:: TextAlignment.Natural

.. _control-size-consts:

ControlSize constants
---------------------

.. data:: ControlSize.Regular
.. data:: ControlSize.Small
.. data:: ControlSize.Mini

.. _number-style-consts:

NumberStyle constants
---------------------

.. data:: NumberStyle.NoStyle
.. data:: NumberStyle.Decimal
.. data:: NumberStyle.Currency
.. data:: NumberStyle.Percent
.. data:: NumberStyle.Scientific
.. data:: NumberStyle.SpellOut

.. _shortcut-key-consts:

Special shortcut keys
---------------------

Menu shortcuts with special keys can be created with these special itentifiers:

.. data:: return
.. data:: enter
.. data:: backspace
.. data:: esc
.. data:: arrowup
.. data:: arrowdown
.. data:: arrowleft
.. data:: arrowright
