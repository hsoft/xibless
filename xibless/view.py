from .base import GeneratedItem

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    
    def __init__(self, parent, rect):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.setup = "$viewsetup$\n$addtoparent$\n"
        tmpl.allocinit = "$classname$ *$varname$ = [[$classname$ alloc] initWithFrame:NSMakeRect($rect$)];"
        tmpl.viewsetup = ''
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl
    
