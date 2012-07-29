from .base import const
from .property import Property
from .control import Control, ControlHeights

class Slider(Control):
    OBJC_CLASS = 'NSSlider'
    PROPERTIES = Control.PROPERTIES + [
        'minValue', 'maxValue', Property('value', 'intValue'), 'numberOfTickMarks',
        'tickMarkPosition', 'allowsTickMarkValuesOnly',
    ]
    
    def __init__(self, parent, minValue, maxValue, value=0):
        self.minValue = minValue
        self.maxValue = maxValue
        self.value = value
        self.tickMarkCount = 0
        Control.__init__(self, parent, 100, 20)
    
    def _getControlHeights(self):
        if self.tickMarkCount > 0:
            return ControlHeights(24, 17, 16)
        else:
            return ControlHeights(17, 13, 11)
    
    def _updateLayoutDeltas(self):
        controlSize = self._controlSize
        # Whether there are tickmarks or not, horizontal deltas are the same
        if controlSize == const.NSRegularControlSize:
            self.layoutDeltaX = -2
            self.layoutDeltaW = 4
        else:
            self.layoutDeltaX = 0
            self.layoutDeltaW = 0
        if self.tickMarkCount > 0:
            self.layoutDeltaY = -2
            self.layoutDeltaH = 2
            if controlSize == const.NSSmallControlSize:
                self.layoutDeltaY = -1
                self.layoutDeltaH = 1
            elif controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = 0
                self.layoutDeltaH = 0
        else:
            self.layoutDeltaY = -2
            self.layoutDeltaH = 4
            if controlSize == const.NSSmallControlSize:
                self.layoutDeltaY = -2
                self.layoutDeltaH = 2
            elif controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = -1
                self.layoutDeltaH = 1
    
