from .base import const
from .property import Property
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
    PROPERTIES = Control.PROPERTIES + [
        Property('text', 'stringValue'), 'textColor', 
        Property('placeholder', 'cell.placeholderString'),
    ]
    
    def __init__(self, parent, text):
        Control.__init__(self, parent, 100, 22)
        self.text = text
        self.font = Font(FontFamily.Label, FontSize.RegularControl)
        self.alignment = None
        self.textColor = None
    
    def dependencies(self):
        return Control.dependencies(self) + [self.textColor]
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        self.properties['editable'] = True
        self.properties['selectable'] = True
        self.properties['alignment'] = TextAlignment.objcValue(self.alignment)
        return tmpl
    

class Label(TextField):
    CONTROL_HEIGHTS = ControlHeights(17, 14, 11)
    
    def __init__(self, parent, text):
        TextField.__init__(self, parent, text)
        self.height = 17
        
        self.layoutDeltaX = -3
        self.layoutDeltaY = 0
        self.layoutDeltaW = 6
        self.layoutDeltaH = 0
    
    def generateInit(self):
        tmpl = TextField.generateInit(self)
        self.properties['editable'] = False
        self.properties['selectable'] = False
        self.properties['drawsBackground'] = False
        self.properties['bordered'] = False
        return tmpl
    

class SearchField(TextField):
    OBJC_CLASS = 'NSSearchField'
    PROPERTIES = TextField.PROPERTIES + [
        Property('sendsWholeSearchString', 'cell.sendsWholeSearchString'),
        Property('searchesImmediately', 'cell.sendsSearchStringImmediately'),
    ]
    
    def __init__(self, parent, placeholder):
        TextField.__init__(self, parent, None)
        self.placeholder = placeholder
    
