from .textfield import TextField

class Label(TextField):
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
    
