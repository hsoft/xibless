from __future__ import division

from collections import namedtuple, defaultdict

from .base import GeneratedItem, Literal

class Pack(object):
    # Corners
    UpperLeft = 1
    UpperRight = 2
    LowerLeft = 3
    LowerRight = 4

    # Sides / Align
    Left = 5
    Right = 6
    Above = 7
    Below = 8
    Middle = 9
    
    @staticmethod
    def oppositeSide(side):
        if side == Pack.Left:
            return Pack.Right
        elif side == Pack.Right:
            return Pack.Left
        elif side == Pack.Above:
            return Pack.Below
        elif side == Pack.Below:
            return Pack.Above

Anchor = namedtuple('Anchor', 'corner growX growY')

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    
    BORDER_MARGIN = 20
    INTER_VIEW_MARGIN = 8
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
        self.anchor = Anchor(Pack.UpperLeft, False, False)
        # a mapping PackingSide: {views} which is used in fill() to know how much we can fill
        self.neighbors = defaultdict(set)
    
    #--- Pack
    def packToCorner(self, corner):
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        margin = self.BORDER_MARGIN
        if corner in (Pack.LowerLeft, Pack.UpperLeft):
            x = margin
        else:            
            x = pw - margin - w
        if corner in (Pack.LowerLeft, Pack.LowerRight):
            y = margin
        else:            
            y = ph - margin - h
        self.x, self.y = x, y
    
    def packRelativeTo(self, other, side, align):
        assert other.parent is self.parent
        ox, oy, ow, oh = other.rect
        x, y, w, h = self.rect
        margin = self.INTER_VIEW_MARGIN
        
        if side in (Pack.Above, Pack.Below):
            if align == Pack.Left:
                x = ox
            elif align == Pack.Right:
                x = ox + ow - w
            else:
                x = ox + ((ow - w) / 2)
        elif side == Pack.Left:
            x = ox - margin - w
        else:
            x = ox + ow + margin
        if side in (Pack.Left, Pack.Right):
            if align == Pack.Below:
                y = oy
            elif align == Pack.Above:
                y = oy + oh - h
            else:
                y = oy + ((oh - h) / 2)
        elif side == Pack.Above:
            y = oy + oh + margin
        else:
            y = oy - margin - h
        self.x, self.y = x, y
        self.neighbors[Pack.oppositeSide(side)].add(other)
        other.neighbors[side].add(self)
    
    def setAnchor(self, corner, growX=False, growY=False):
        self.anchor = Anchor(corner, growX, growY)
    
    def fill(self, side):
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        neighbors = self.neighbors[side]
        margin = self.BORDER_MARGIN
        if side == Pack.Right:
            nx = max([(n.x + n.width) for n in neighbors] + [x+w])
            goal = pw - margin
            growby = goal - nx
            w += growby
            for n in neighbors:
                n.x += growby
        elif side == Pack.Left:
            nx = min([n.x for n in neighbors] + [x])
            goal = margin
            growby = nx - goal
            w += growby
            x -= growby
            for n in neighbors:
                n.x -= growby
        else:
            raise Exception("Vertical fill not supported yet")
        self.x, self.y, self.width, self.height = x, y, w, h
    
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
        if self.anchor.growX and self.anchor.growY:
            resizeMask = 'NSViewWidthSizable|NSViewHeightSizable'
        elif self.anchor.growX:
            if self.anchor.corner in (Pack.LowerLeft, Pack.LowerRight):
                resizeMask = 'NSViewWidthSizable|NSViewMaxYMargin'
            else:
                resizeMask = 'NSViewWidthSizable|NSViewMinYMargin'
        elif self.anchor.growY:
            if self.anchor.corner in (Pack.UpperLeft, Pack.LowerLeft):
                resizeMask = 'NSViewHeightSizable|NSViewMaxXMargin'
            else:
                resizeMask = 'NSViewHeightSizable|NSViewMinXMargin'
        else:
            if self.anchor.corner == Pack.LowerLeft:
                resizeMask = 'NSViewMaxXMargin|NSViewMaxYMargin'
            elif self.anchor.corner == Pack.UpperRight:
                resizeMask = 'NSViewMinXMargin|NSViewMinYMargin'
            elif self.anchor.corner == Pack.LowerRight:
                resizeMask = 'NSViewMinXMargin|NSViewMaxYMargin'
            else:
                resizeMask = 'NSViewMaxXMargin|NSViewMinYMargin'
        self.properties['autoresizingMask'] = Literal(resizeMask)
        if self.parent is not None:
            tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl
    
    def generateAddSubview(self, subview):
        return "[[%s contentView] addSubview:%s];\n" % (self.varname, subview.varname)
    
    @property
    def rect(self):
        return self.x, self.y, self.width, self.height
