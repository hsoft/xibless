from .textfield import TextField

class Label(TextField):
    LAYOUT_DELTA_X = -3
    LAYOUT_DELTA_W = 6
    
    def __init__(self, parent, text):
        TextField.__init__(self, parent, text)
        self.width = 17
    
    def generateInit(self):
        tmpl = TextField.generateInit(self)
        self.properties['editable'] = False
        self.properties['selectable'] = False
        self.properties['drawsBackground'] = False
        self.properties['bordered'] = False
        return tmpl
    
