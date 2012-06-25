from .view import View

class Label(View):
    OBJC_CLASS = 'NSTextField'
    
    def __init__(self, parent, rect, text):
        View.__init__(self, parent, rect)
        self.text = text
        self.font = None
    
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
    
