from .view import View
from .font import Font, FontFamily, FontSize

class TextField(View):
    OBJC_CLASS = 'NSTextField'
    
    DEFAULT_FONT = Font(FontFamily.Label, FontSize.RegularControl)
    
    def __init__(self, parent, text):
        View.__init__(self, parent, 100, 22)
        self.text = text
        self.font = self.DEFAULT_FONT
        self.alignment = None
        self.textColor = None
    
    def dependencies(self):
        return [self.font, self.textColor]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['stringValue'] = self.text
        self.properties['font'] = self.font
        self.properties['editable'] = True
        self.properties['selectable'] = True
        self.properties['alignment'] = self.alignment
        self.properties['textColor'] = self.textColor
        return tmpl
    
