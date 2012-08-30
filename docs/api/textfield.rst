TextField
=========

The ``Textfield`` is a :class:`Control` subclass that represents Cocoa's ``NSTextField``.

.. class:: TextField(parent[, text])
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param text: String. See :attr:`text`.
    
    .. attribute:: text
        
        A string that represents the text field's text. Equivalent to ``[self stringValue]``.
    
    .. attribute:: placeholder
        
        A string representing the "placeholder text", that is, a text displayed in light shade of
        grey when the text field contains no text. Equivalent to ``[[self cell] placeholderString]``.
    
    .. attribute:: alignment
        
        One of :ref:`text-alignment-constants`. Alignment of the text within the field.
        Equivalent to ``[self alignment]``.
    
    .. attribute:: textColor
        
        :class:`Color`. Color of the text within the field. Equivalent to ``[self textColor]``.
    
    .. attribute:: fixedHeight
    
        *Boolean*. ``TextField``, being a :class:`Control` subclass, has its height governed by
        :attr:`Control.controlSize`. This means that any layout method that would otherwise change
        a view's height (for example, :meth:`View.fill`) will not do it for a ``Control``. However,
        in some cases, you want a text field to have a variable height because you want it to be
        multi-line. In these cases, set this attribute to ``False`` to indicate that
        height-modyifing layout methods can affect this view.

Label
-----

The ``Label`` is a :class:`TextField` subclass that mimics the presentation of the label in XCode,
that is, uneditable, unselectable, borderless and backgroundless.

.. class:: Label(parent, text)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param text: String. See :attr:`TextField.text`.

SearchField
-----------

A subclass of :class:`TextField` that wraps ``NSSearchField``. Note the slightly different
initialization signature: instead of ``text``, the second argument is ``placeholder`` because it's
very rare that we initalize a search field with text. We usually do so with a placeholder string.

.. class:: SearchField(parent, placeholder)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param placeholder: String. See :attr:`TextField.placeholder`.
    
    .. attribute:: sendsWholeSearchString
    
        *Boolean*. Whether the search action is triggered after each keystroke or when the user
        presses return. In Cocoa: ``cell.sendsWholeSearchString``.
    
    .. attribute:: searchesImmediately
        
        *Boolean*. Whether there's a small delay between the keystroke and the search field action
        triggering. In Cocoa: ``cell.sendsSearchStringImmediately``.

Combobox
--------

The ``Combobox`` is a :class:`TextField` subclass that represents Cocoa's ``NSComboBox``.

.. class:: Combobox(parent[, items=None])

    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    :param items: A list of strings. See :attr:`items`
    
    .. attribute:: items
        
        A list of strings determining the items that will be present in the combobox's dropdown.
    
    .. attribute:: autoCompletes
        
        A boolean telling whether the combobox autocompletes. Equivalent to ``[self completes]``.
