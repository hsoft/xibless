from .view import View
from .font import Font, FontFamily, FontSize

class TextField(View):
    OBJC_CLASS = 'NSTextField'
    
    DEFAULT_FONT = Font(FontFamily.Label, FontSize.RegularControl)
    
    def __init__(self, parent, text):
        View.__init__(self, parent, 100, 22)
        self.text = text
        self.font = self.DEFAULT_FONT
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['stringValue'] = self.text
        self.properties['font'] = self.font
        self.properties['editable'] = True
        self.properties['selectable'] = True
        return tmpl
    
