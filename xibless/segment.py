from .control import Control, ControlHeights
from .base import const, convertValueToObjc
from .types import NLSTR
from .property import Property

class Segment(object):
    def __init__(self, label, width):
        self.label = label
        self.width = width
        self.image = None
        self.accessibilityDescription = None
    

class SegmentedControl(Control):
    OBJC_CLASS = 'NSSegmentedControl'
    CONTROL_HEIGHTS = ControlHeights(22, 18, 15)
    PROPERTIES = Control.PROPERTIES + [
        'segmentStyle', Property('trackingMode', 'cell.trackingMode'),
    ]
    
    def __init__(self, parent):
        Control.__init__(self, parent, 25, 25)
        self.segments = []
    
    def _updateLayoutDeltas(self):
        controlSize = self._controlSize
        self.layoutDeltaX = 0
        self.layoutDeltaY = -2
        self.layoutDeltaW = 0
        self.layoutDeltaH = 3
        if controlSize == const.NSSmallControlSize:
            self.layoutDeltaY = -1
            self.layoutDeltaH = 1
        if controlSize == const.NSMiniControlSize:
            self.layoutDeltaY = -1
            self.layoutDeltaH = 2
    
    def _adjustWidth(self):
        segmentsWidth = sum(s.width for s in self.segments)
        overhead = 8
        self.width = segmentsWidth + overhead
     
    def addSegment(self, label, width):
        result = Segment(label, width)
        self.segments.append(result)
        self._adjustWidth()
        return result
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        tmpl.setup += self.accessor._callMethod('setSegmentCount', len(self.segments))
        for index, segment in enumerate(self.segments):
            tmpl.setup += '[$varname$ setLabel:{} forSegment:{}];\n'.format(
                convertValueToObjc(segment.label), convertValueToObjc(index))
            tmpl.setup += '[$varname$ setWidth:{} forSegment:{}];\n'.format(
                convertValueToObjc(segment.width), convertValueToObjc(index))
            if segment.image:
                tmpl.setup += '[$varname$ setImage:[NSImage imageNamed:{}] forSegment:{}];\n'.format(
                convertValueToObjc(NLSTR(segment.image)), convertValueToObjc(index))
            if segment.accessibilityDescription:
                tmpl.setup += 'setAccessibilityDescriptionOfChild($varname$, {}, {});\n'.format(
                    convertValueToObjc(index), convertValueToObjc(segment.accessibilityDescription))
        return tmpl
