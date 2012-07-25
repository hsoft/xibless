from .base import convertValueToObjc, const, Literal, KeyValueId, NonLocalizableString
from .control import Control, ControlHeights
from .menu import Menu

class Popup(Control):
    OBJC_CLASS = 'NSPopUpButton'
    CONTROL_HEIGHTS = ControlHeights(26, 22, 15)
    PROPERTIES = Control.PROPERTIES + ['menu']
    
    def __init__(self, parent, items=None):
        Control.__init__(self, parent, 100, 20)
        self.menu = Menu('')
        if items:
            for item in items:
                self.menu.addItem(item)
        self.pullsdown = False
    
    def _updateLayoutDeltas(self):
        controlSize = self._controlSize
        self.layoutDeltaX = -3
        self.layoutDeltaY = -3
        self.layoutDeltaW = 6
        self.layoutDeltaH = 5
        if controlSize == const.NSSmallControlSize:
            self.layoutDeltaY = -3
            self.layoutDeltaH = 4
        elif controlSize == const.NSMiniControlSize:
            self.layoutDeltaY = 0
            self.layoutDeltaH = 0
    
    def dependencies(self):
        return Control.dependencies(self) + [self.menu]
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        tmpl.initmethod = "initWithFrame:$rect$ pullsDown:$pullsdown$"
        tmpl.pullsdown = convertValueToObjc(self.pullsdown)
        return tmpl
