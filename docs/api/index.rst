xibless API
===========

This is the API documentation for each class in ``xibless``. Classes in the API documentation
contain methods, which can of course be called, but they also contain attributes (such as ``x``,
``y``, ``font``, etc.). These can be set directly in this fashion::

    button.x = 42


**How to read the API.** Being a wrapper around Cocoa, there are naturally a lot of attribute names
that are similar to their Cocoa counterpart. When a class has an attribute that doesn't specify
what attribute it wraps in Cocoa, you can assume that it wraps an attribute with the exact same
name.

Contents:

.. toctree::
   :maxdepth: 2
   
   types
   const
   view
   layout
   control
   formatter
   window
   menu
   button
   textfield
   textview
   popup
   radio
   progress
   image
   tabview
   table
   splitview
   segment
   slider
   toolbar
