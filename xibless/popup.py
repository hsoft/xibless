from .base import convertValueToObjc
from .view import View
from .menu import Menu

class Popup(View):
    OBJC_CLASS = 'NSPopUpButton'
    
    def __init__(self, parent, items=None):
        View.__init__(self, parent, 100, 20)
        self.menu = Menu('')
        if items:
            for item in items:
                self.menu.addItem(item)
        self.pullsdown = False
        
        self.layoutDeltaX = -3
        self.layoutDeltaY = -4
        self.layoutDeltaW = -6
        self.layoutDeltaH = 6
    
    def dependencies(self):
        return [self.menu]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.allocinit = "$classname$ *$varname$ = [[[$classname$ alloc] initWithFrame:$rect$ pullsDown:$pullsdown$] autorelease];"
        tmpl.pullsdown = convertValueToObjc(self.pullsdown)
        self.properties['menu'] = self.menu
        return tmpl
