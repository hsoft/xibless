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
    
    # About coordinates: The coordinates below are "Layout coordinates". They will be slightly
    # adjusted at generation time.
    # According to http://www.cocoabuilder.com/archive/cocoa/192607-interface-builder-layout-versus-frame.html
    # the difference between "Frame Rectangle" and "Layout Rectangle" are hardcoded in IB, so we
    # need to maintain our own hardcoded constants for each supported widget.
    LAYOUT_DELTA_X = 0
    LAYOUT_DELTA_Y = 0
    LAYOUT_DELTA_W = 0
    LAYOUT_DELTA_H = 0
    
    def __init__(self, parent, width, height):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
    
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
        self.x, self.y = x, y
    
    def packRelativeTo(self, other, side):
        assert other.parent is self.parent
        ox, oy, ow, oh = other.rect
        x, y, w, h = self.rect
        margin = 8
        if side in (Pack.Above, Pack.Under):
            x = ox
        elif side == Pack.Left:
            x = ox - margin - w
        else:
            x = ox + ow + margin
        if side in (Pack.Left, Pack.Right):
            y = oy
        elif side == Pack.Above:
            y = oy + oh + margin
        else:
            y = oy - margin - h
        self.x, self.y = x, y
    
    #--- Generate
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.setup = "$viewsetup$\n$addtoparent$\n"
        tmpl.allocinit = "$classname$ *$varname$ = [[$classname$ alloc] initWithFrame:$rect$];"
        x, y, w, h = self.x, self.y, self.width, self.height
        x += self.LAYOUT_DELTA_X
        y += self.LAYOUT_DELTA_Y
        w += self.LAYOUT_DELTA_W
        h += self.LAYOUT_DELTA_H
        tmpl.rect = "NSMakeRect(%d, %d, %d, %d)" % (x, y, w, h)
        if self.parent is not None:
            tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl
    
    def generateAddSubview(self, subview):
        return "[[%s contentView] addSubview:%s];\n" % (self.varname, subview.varname)
    
    @property
    def rect(self):
        return self.x, self.y, self.width, self.height
