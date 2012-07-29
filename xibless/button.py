from .control import Control, ControlHeights
from .base import const
from .types import NLSTR
from .property import ImageProperty
from .view import Pack
from .table import TableView
from .tabview import TabView

class Button(Control):
    OBJC_CLASS = 'NSButton'
    PROPERTIES = Control.PROPERTIES + ['imagePosition', ImageProperty('image')]
    
    def __init__(self, parent, title, action=None):
        self._bezelStyle = const.NSRoundedBezelStyle
        Control.__init__(self, parent, 80, 20)
        self.buttonType = const.NSMomentaryLightButton
        self.state = None
        self.title = title
        self.keyEquivalent = None
        self.action = action
        self.image = None
        self._updateLayoutDeltas()
    
    def _getControlHeights(self):
        if self.bezelStyle == const.NSTexturedRoundedBezelStyle:
            return ControlHeights(22, 18, 15)
        elif self.bezelStyle == const.NSRoundRectBezelStyle:
            return ControlHeights(18, 16, 14)
        else:
            return ControlHeights(21, 18, 15)
    
    def _getControlFontSize(self, controlSize):
        bezelStyle = self.bezelStyle
        if (bezelStyle == const.NSRoundRectBezelStyle) and (controlSize == const.NSRegularControlSize):
            return 12
        else:
            return Control._getControlFontSize(self, controlSize)
    
    def _updateLayoutDeltas(self):
        bezelStyle = self._bezelStyle
        controlSize = self._controlSize
        if bezelStyle == const.NSRoundRectBezelStyle:
            self.layoutDeltaX = 0
            self.layoutDeltaY = -1
            self.layoutDeltaW = 0
            self.layoutDeltaH = 1
            if controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = -2
                self.layoutDeltaH = 3 
        elif bezelStyle == const.NSTexturedRoundedBezelStyle:
            self.layoutDeltaX = 0
            self.layoutDeltaY = -1
            self.layoutDeltaW = 0
            self.layoutDeltaH = 3
            if controlSize == const.NSSmallControlSize:
                self.layoutDeltaY = -2
                self.layoutDeltaH = 2
            elif controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = 0
                self.layoutDeltaH = 0
        else:
            self.layoutDeltaX = -6
            self.layoutDeltaY = -7
            self.layoutDeltaW = 12
            self.layoutDeltaH = 11
            if controlSize == const.NSSmallControlSize:
                self.layoutDeltaY = -6
                self.layoutDeltaH = 10
            elif controlSize == const.NSMiniControlSize:
                self.layoutDeltaY = -1
                self.layoutDeltaH = 1
    
    @property
    def bezelStyle(self):
        return self._bezelStyle
    
    @bezelStyle.setter
    def bezelStyle(self, value):
        self._bezelStyle = value
        self._updateControlSize()
        self._updateLayoutDeltas()
    
    def outerMargin(self, other, side):
        # Push buttons have special vertical margins
        if self.bezelStyle == const.NSRoundedBezelStyle and side in (Pack.Above, Pack.Below):
            if other.isOrHas(Button, side):
                # If it's two Push buttons, the margin is 12. If it's a push button and another type
                # of button, it's 20. If it's a push button and another type of view, it's the
                # normal 8. If it's a layout (thus not a Button instance), we don't consider the
                # "2 push buttons" special case at all.
                if isinstance(other, Button) and other.bezelStyle == const.NSRoundedBezelStyle:
                    # two push buttons, it's 12 both horizontally and vertically
                    return 12
                elif side in (Pack.Above, Pack.Below):
                    # A push button and another style of button, the vertical margin is 20
                    return 20
            elif other.isOrHas(TableView, side):
                # A push button under a table has 20 of margin
                return 20
            elif other.isOrHas(TabView, side):
                # A push button under a tab view has a margin of 10
                return 10
        return Control.outerMargin(self, other, side)
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        self.properties['title'] = self.title
        self.properties['buttonType'] = self.buttonType
        self.properties['bezelStyle'] = self.bezelStyle
        self.properties['state'] = self.state
        if self.keyEquivalent:
            self.properties['keyEquivalent'] = NLSTR(self.keyEquivalent)
        return tmpl
    

class Checkbox(Button):
    CONTROL_HEIGHTS = ControlHeights(14, 14, 10)
    
    def __init__(self, parent, title):
        Button.__init__(self, parent, title)
        self.buttonType = const.NSSwitchButton
        self.bezelStyle = const.NSRegularSquareBezelStyle
        
        self.layoutDeltaX = -2
        self.layoutDeltaY = -2
        self.layoutDeltaW = 4
        self.layoutDeltaH = 4
    
    def generateInit(self):
        tmpl = Button.generateInit(self)
        self.properties['imagePosition'] = const.NSImageLeft
        
        return tmpl
