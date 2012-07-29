from .types import stringArray
from .textfield import TextField

class Combobox(TextField):
    OBJC_CLASS = 'NSComboBox'
    
    def __init__(self, parent, items=None):
        TextField.__init__(self, parent, "")
        self.height = 20
        self.items = items
        self.autoComplete = False
        
        self.layoutDeltaX = 0
        self.layoutDeltaY = -4
        self.layoutDeltaW = 3
        self.layoutDeltaH = 6
    
    def generateInit(self):
        tmpl = TextField.generateInit(self)
        if self.items:
            array = stringArray(self.items)
            tmpl.viewsetup = "[$varname$ addItemsWithObjectValues:%s];\n" % array
        self.properties['completes'] = self.autoComplete
        return tmpl
