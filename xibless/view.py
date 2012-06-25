from .base import GeneratedItem

class Pack(object):
    # Corners
    UpperLeft = 1
    UpperRight = 2
    LowerLeft = 3
    LowerRight = 4

    # Sides
    Left = 5
    Right = 6
    Above = 7
    Under = 8

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    
    def __init__(self, parent, rect):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
    
    #--- Pack
    def packToCorner(self, corner):
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        margin = 20
        if corner in (Pack.LowerLeft, Pack.UpperLeft):
            x = margin
        else:            
            x = pw - margin - w
        if corner in (Pack.LowerLeft, Pack.LowerRight):
            y = margin
        else:            
            y = ph - margin - h
        self.rect = (x, y, w, h)
    
    #--- Generate
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
    
