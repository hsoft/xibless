from .base import convertValueToObjc
from .view import View
from .menu import Menu

class Popup(View):
    OBJC_CLASS = 'NSPopUpButton'
    
    LAYOUT_DELTA_X = -3
    LAYOUT_DELTA_Y = -4
    LAYOUT_DELTA_W = -6
    LAYOUT_DELTA_H = 6
    
    def __init__(self, parent, items=None):
        View.__init__(self, parent, 100, 20)
        self.menu = Menu('')
        if items:
            for item in items:
                self.menu.addItem(item)
        self.pullsdown = False
        
    
    def dependencies(self):
        return [self.menu]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.allocinit = "$classname$ *$varname$ = [[$classname$ alloc] initWithFrame:$rect$ pullsDown:$pullsdown$];"
        tmpl.pullsdown = convertValueToObjc(self.pullsdown)
        self.properties['menu'] = self.menu
        return tmpl
