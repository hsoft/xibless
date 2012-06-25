from .view import View
from .font import Font, FontFamily, FontSize

class Label(View):
    OBJC_CLASS = 'NSTextField'
    
    LAYOUT_DELTA_X = -3
    LAYOUT_DELTA_W = 6
    
    DEFAULT_FONT = Font(FontFamily.Label, FontSize.RegularControl)
    
    def __init__(self, parent, text):
        View.__init__(self, parent, 100, 17)
        self.text = text
        self.font = self.DEFAULT_FONT
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['stringValue'] = self.text
        self.properties['font'] = self.font
        self.properties['editable'] = False
        self.properties['selectable'] = False
        self.properties['drawsBackground'] = False
        self.properties['bordered'] = False
        return tmpl
    
