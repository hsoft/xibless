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
        tmpl.allocinit = "$classname$ *$varname$ = [[$classname$ alloc] initWithFrame:$rect$];"
        tmpl.rect = "NSMakeRect(%d, %d, %d, %d)" % self.rect
        if self.parent is not None:
            tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl
    
    def generateAddSubview(self, subview):
        return "[[%s contentView] addSubview:%s];\n" % (self.varname, subview.varname)
    
