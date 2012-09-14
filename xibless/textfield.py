from .property import Property
from .control import Control, ControlHeights
from .font import Font, FontFamily, FontSize

class TextField(Control):
    OBJC_CLASS = 'NSTextField'
    CONTROL_HEIGHTS = ControlHeights(22, 19, 16)
    PROPERTIES = Control.PROPERTIES + [
        Property('text', 'stringValue'), 'textColor', 
        Property('placeholder', 'cell.placeholderString'),
        Property('usesSingleLineMode', 'cell.usesSingleLineMode')
    ]
    
    def __init__(self, parent, text=None):
        Control.__init__(self, parent, 100, 22)
        self.text = text
        self.font = Font(FontFamily.Label, FontSize.RegularControl)
        self.textColor = None
        self.usesSingleLineMode = False
    
    def dependencies(self):
        return Control.dependencies(self) + [self.textColor]
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        self.properties['editable'] = True
        self.properties['selectable'] = True
        # By default in IB, a textfield is scrollable. This allows a smooth overflow management.
        # If it's false, as soon as you type a character that overflows the field, the whole line
        # disappears and is replaced by the new character. With scrollable to True, the text scrolls
        # and makes editing smoother.
        # In xibless, we differ a bit from XCode's default behavior in that by default, a textfield
        # wraps (in XCode, it scrolls by default and you have to explicitly tell it to wrap). We
        # want most textfields (particularly labels) to wrap.
        # However, if usesSingleLineMode is True, we scroll because that's the behavior that makes
        # the most sense.
        if self.usesSingleLineMode:
            self.properties['cell.scrollable'] = True
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
    
