from .control import Control, ControlHeights
from .base import const
from .font import Font, FontFamily, FontSize
from .view import Pack

class Button(Control):
    OBJC_CLASS = 'NSButton'
    
    def __init__(self, parent, title, action=None):
        Control.__init__(self, parent, 80, 20)
        self.buttonType = const.NSMomentaryLightButton
        # Layout deltas and font are set in bezelStyle setter
        self.bezelStyle = const.NSRoundedBezelStyle
        self.state = None
        self.title = title
        self.action = action
        self.keyEquivalent = None
        
    
    @property
    def bezelStyle(self):
        return self._bezelStyle
    
    @bezelStyle.setter
    def bezelStyle(self, value):
        self._bezelStyle = value
        if value == const.NSRoundRectBezelStyle:
            self.layoutDeltaX = 0
            self.layoutDeltaY = 0
            self.layoutDeltaW = 0
            self.layoutDeltaH = 1
            self.font = Font(FontFamily.System, 12)
        else:
            self.layoutDeltaX = -6
            self.layoutDeltaY = -8
            self.layoutDeltaW = 12
            self.layoutDeltaH = 12
            self.font = Font(FontFamily.System, FontSize.RegularControl)
    
    def outerMargin(self, other, side):
        if isinstance(other, Button) and self.bezelStyle == const.NSRoundedBezelStyle \
                and other.bezelStyle == const.NSRoundedBezelStyle \
                and side in (Pack.Left, Pack.Right):
            return 12
        else:
            return Control.outerMargin(self, other, side)
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        self.properties['title'] = self.title
        self.properties['buttonType'] = self.buttonType
        self.properties['bezelStyle'] = self.bezelStyle
        self.properties['state'] = self.state
        self.properties['keyEquivalent'] = self.keyEquivalent
        tmpl.viewsetup = "$linkaction$\n"
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
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
