from .base import convertValueToObjc, const
from .property import Property
from .button import Button
from .menu import Menu

class Popup(Button):
    OBJC_CLASS = 'NSPopUpButton'
    PROPERTIES = Button.PROPERTIES + [Property('arrowPosition', 'cell.arrowPosition')]
    
    def __init__(self, parent, items=None):
        Button.__init__(self, parent, '')
        self.menu = Menu('')
        if items:
            for item in items:
                self.menu.addItem(item)
        self.pullsdown = False
    
    def _updateLayoutDeltas(self):
        bezelStyle = self._bezelStyle
        controlSize = self._controlSize
        if bezelStyle == const.NSRoundRectBezelStyle:
            Button._updateLayoutDeltas(self) # exactly the same as Button
        elif bezelStyle == const.NSTexturedRoundedBezelStyle:
            self.layoutDeltaX = 0
            self.layoutDeltaY = -2
            self.layoutDeltaW = 0
            self.layoutDeltaH = 3
            if controlSize == const.NSSmallControlSize:
                self.layoutDeltaY = 0
                self.layoutDeltaH = 0
            elif controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = -1
                self.layoutDeltaH = 2
        else:
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
        return Button.dependencies(self) + [self.menu]
    
    def generateInit(self):
        tmpl = Button.generateInit(self)
        tmpl.initmethod = "initWithFrame:$rect$ pullsDown:$pullsdown$"
        tmpl.pullsdown = convertValueToObjc(self.pullsdown)
        return tmpl
