from .base import const
from .control import Control, ControlHeights
from .font import Font, FontFamily, FontSize

class TextAlignment(object):
    Left = 1
    Right = 2
    Center = 3
    Justified = 4
    Natural = 5
    
    @staticmethod
    def objcValue(value):
        if value == TextAlignment.Left:
            return const.NSLeftTextAlignment
        elif value == TextAlignment.Right:
            return const.NSRightTextAlignment
        elif value == TextAlignment.Center:
            return const.NSCenterTextAlignment
        elif value == TextAlignment.Justified:
            return const.NSJustifiedTextAlignment
        elif value == TextAlignment.Natural:
            return const.NSNaturalTextAlignment
        else:
            return value

class TextField(Control):
    OBJC_CLASS = 'NSTextField'
    CONTROL_HEIGHTS = ControlHeights(22, 19, 16)
    
    def __init__(self, parent, text):
        Control.__init__(self, parent, 100, 22)
        self.text = text
        self.font = Font(FontFamily.Label, FontSize.RegularControl)
        self.alignment = None
        self.textColor = None
    
    def dependencies(self):
        return [self.font, self.textColor]
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        self.properties['stringValue'] = self.text
        self.properties['editable'] = True
        self.properties['selectable'] = True
        self.properties['alignment'] = TextAlignment.objcValue(self.alignment)
        self.properties['textColor'] = self.textColor
        return tmpl
    
