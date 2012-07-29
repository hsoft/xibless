from .base import const
from .property import Property
from .view import View

class ProgressIndicator(View):
    OBJC_CLASS = 'NSProgressIndicator'
    PROPERTIES = View.PROPERTIES + [
        'style', 'controlSize', 'minValue', 'maxValue', 'indeterminate', 'displayedWhenStopped',
        Property('value', 'doubleValue'),
    ]
    
    def __init__(self, parent):
        View.__init__(self, parent, 92, 16)
        self.style = const.NSProgressIndicatorBarStyle
        self.minValue = 0
        self.maxValue = 100
        self.value = 0
        self.indeterminate = True
        self.displayedWhenStopped = True
        self._controlSize = None
        
        self.layoutDeltaX = -2
        self.layoutDeltaY = 0
        self.layoutDeltaW = 4
        self.layoutDeltaH = 5
    
    @property
    def controlSize(self):
        return self._controlSize
    
    @controlSize.setter
    def controlSize(self, value):
        if value == const.NSMiniControlSize: # not supported
            value = const.NSSmallControlSize
        self._controlSize = value
        if value == const.NSSmallControlSize:
            if self.style == const.NSProgressIndicatorBarStyle:
                self.height = 10
            else:
                self.width = self.height = 16
        else: # regular
            if self.style == const.NSProgressIndicatorBarStyle:
                self.height = 16
            else:
                self.width = self.height = 32
    
