from .base import GeneratedItem

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    
    def __init__(self, parent, rect):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
    
    def generateInit(self):
        tmpl = self.template("""$classname$ *$varname$ = $allocinit$;
        $viewsetup$
        $addtoparent$
        """)
        tmpl.classname = self.OBJC_CLASS
        tmpl.allocinit = "[[$classname$ alloc] initWithFrame:NSMakeRect($rect$)]"
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl
    
