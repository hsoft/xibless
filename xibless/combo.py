from .base import convertValueToObjc
from .textfield import TextField

class Combobox(TextField):
    OBJC_CLASS = 'NSComboBox'
    
    LAYOUT_DELTA_X = 0
    LAYOUT_DELTA_Y = -4
    LAYOUT_DELTA_W = 3
    LAYOUT_DELTA_H = 6
    
    def __init__(self, parent, items=None):
        TextField.__init__(self, parent, "")
        self.height = 20
        self.items = items
        self.autoComplete = False
    
    def generateInit(self):
        tmpl = TextField.generateInit(self)
        if self.items:
            array = "[NSArray arrayWithObjects:%s,nil]" % ','.join(convertValueToObjc(item) for item in self.items)
            tmpl.viewsetup = "[$varname$ addItemsWithObjectValues:%s];\n" % array
        self.properties['completes'] = self.autoComplete
        return tmpl
