Slider
======

A :class:`Control` subclass that wraps Cocoa's ``NSSlider``.

.. class:: Slider(parent, minValue, maxValue[, value])
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`
    :param minValue: *Numeric*. See :attr:`minValue`
    :param maxValue: *Numeric*. See :attr:`maxValue`
    :param value: *Numeric*. See :attr:`value`
    
    .. attribute:: minValue
        
        *Numeric*. The value the slider has when its knob is at its minimum.
    
    .. attribute:: maxValue
        
        *Numeric*. The value the slider has when its knob is at its maximum.
    
    .. attribute:: value
        
        *Numeric*. The initial value of the slider. In Cocoa: ``intValue``.
    
    .. attribute:: numberOfTickMarks
        
        *Numeric*. Number of tickmarks along the slider. The apparence of the slider changes if this
        value is 0.
    
    .. attribute:: tickMarkPosition
        
        :ref:`Cocoa constant <literal-consts>`. Where the tickmaks are compared to the slider
        (above or below). Use with ``NSTickMarkPosition`` constants.
    
    .. attribute:: allowsTickMarkValuesOnly
        
        *Boolean*. Whether the slider knob can only set its value to one that exactly matches a
        tickmark.
