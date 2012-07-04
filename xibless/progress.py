from .base import const
from .view import View

class ProgressIndicator(View):
    OBJC_CLASS = 'NSProgressIndicator'
    
    def __init__(self, parent):
        View.__init__(self, parent, 92, 16)
        self.style = const.NSProgressIndicatorBarStyle
        self.minValue = 0
        self.maxValue = 100
        self.value = 0
        self.indeterminate = True
        self.displayedWhenStopped = True
        
        self.layoutDeltaX = -2
        self.layoutDeltaY = 0
        self.layoutDeltaW = 4
        self.layoutDeltaH = 5
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['style'] = self.style
        self.properties['minValue'] = self.minValue
        self.properties['maxValue'] = self.maxValue
        self.properties['doubleValue'] = self.value
        self.properties['indeterminate'] = self.indeterminate
        self.properties['displayedWhenStopped'] = self.displayedWhenStopped
        return tmpl
    
