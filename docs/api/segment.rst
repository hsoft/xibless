SegmentedControl
================

A subclass of :class:`Control` which wraps ``NSSegmentedControl``.

.. class:: SegmentedControl(parent)
    
    :param parent: A :class:`View` instance. See :attr:`View.parent`.
    
    .. attribute:: segmentStyle
        
        :ref:`Cocoa constant <literal-consts>`. Equivalent to ``[self segmentStyle]`` and sets
        the look of the control. Use with ``NSSegmentStyle`` constants.
    
    .. attribute:: trackingMode
    
        :ref:`Cocoa constant <literal-consts>`. Equivalent to ``[[self cell] trackingMode]`` and
        determines whether one, any or no segment can be selected at once. Use with
        ``NSSegmentSwitchTracking`` constants.
    
    .. method:: addSegment(label, width)
        
        :param label: String
        :param width: Numeric
        
        Adds a new segment with the specified label and width and returns it. The width of the
        segmented control will be automatically adjusted to the sum of allsegment widths plus an
        overhead (8).
    

Segment
-------

Represent a segment in a :class:`SegmentedControl`. It doesn't wrap any Cocoa class because none
exist for that, but it still determines how segments in the parent segmented control are going to be
set up. Instantiate with :meth:`SegmentedControl.addSegment`

.. class:: Segment
    
    .. attribute:: label
        
        String. The label of the segment.
    
    .. attribute:: width
        
        Numeric. The width of the segment.
    
