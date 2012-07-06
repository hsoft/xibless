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
    
    @staticmethod
    def side2str(side):
        if side == Pack.Left:
            return 'left'
        elif side == Pack.Right:
            return 'right'
        elif side == Pack.Above:
            return 'above'
        elif side == Pack.Below:
            return 'below'

Anchor = namedtuple('Anchor', 'corner growX growY')

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    
    INNER_MARGIN_LEFT = 20
    INNER_MARGIN_RIGHT = 20
    INNER_MARGIN_ABOVE = 20
    INNER_MARGIN_BELOW = 20
    OUTER_MARGIN_LEFT = 8
    OUTER_MARGIN_RIGHT = 8
    OUTER_MARGIN_ABOVE = 8
    OUTER_MARGIN_BELOW = 8
    
    def __init__(self, parent, width, height):
        GeneratedItem.__init__(self)
        self.parent = parent
        if isinstance(parent, View):
            parent.subviews.append(self)
        self.subviews = []
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.anchor = Anchor(Pack.UpperLeft, False, False)
        # a mapping PackingSide: {views} which is used in fill() to know how much we can fill
        self.neighbors = defaultdict(set)
        
        # About coordinates: The coordinates below are "Layout coordinates". They will be slightly
        # adjusted at generation time.
        # According to http://www.cocoabuilder.com/archive/cocoa/192607-interface-builder-layout-versus-frame.html
        # the difference between "Frame Rectangle" and "Layout Rectangle" are hardcoded in IB, so we
        # need to maintain our own hardcoded constants for each supported widget.
        self.layoutDeltaX = 0
        self.layoutDeltaY = 0
        self.layoutDeltaW = 0
        self.layoutDeltaH = 0
        
    
    #--- Layout
    def outerMargin(self, other, side):
        # The way outer margins (in other words, margins between sibling views) work is that we
        # use the maximum value between the two margins of our views. For example, if a button
        # has a bottom margin of 8 and has a label underneath with a top margin of 7, we use 8.
        # This method will return the appropriate margin if ``other`` is laid at the ``side`` of
        # ``self``. ``side`` can only be onle of the 4 sides (left, right, above, below)
        return getattr(self, 'OUTER_MARGIN_' + Pack.side2str(side).upper())
    
    def innerMargin(self, side):
        return getattr(self, 'INNER_MARGIN_' + Pack.side2str(side).upper())
    
    def packToCorner(self, corner):
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        if corner in (Pack.LowerLeft, Pack.UpperLeft):
            x = self.parent.innerMargin(Pack.Left)
        else:            
            x = pw - self.parent.innerMargin(Pack.Right) - w
        if corner in (Pack.LowerLeft, Pack.LowerRight):
            y = self.parent.innerMargin(Pack.Below)
        else:            
            y = ph - self.parent.innerMargin(Pack.Above) - h
        self.x, self.y = x, y
    
    def packRelativeTo(self, other, side, align=None):
        assert other.parent is self.parent
        ox, oy, ow, oh = other.rect
        x, y, w, h = self.rect
        outerMargin1 = self.outerMargin(other, side)
        outerMargin2 = other.outerMargin(self, Pack.oppositeSide(side))
        outerMargin = max(outerMargin1, outerMargin2)
        
        if align is None:
            align = Pack.Left if side in (Pack.Above, Pack.Below) else Pack.Middle
        
        if side in (Pack.Above, Pack.Below):
            if align == Pack.Left:
                x = ox
            elif align == Pack.Right:
                x = ox + ow - w
            else:
                x = ox + ((ow - w) / 2)
        elif side == Pack.Left:
            x = ox - outerMargin - w
        else:
            x = ox + ow + outerMargin
        if side in (Pack.Left, Pack.Right):
            if align == Pack.Below:
                y = oy
            elif align == Pack.Above:
                y = oy + oh - h
            else:
                y = oy + ((oh - h) / 2)
        elif side == Pack.Above:
            y = oy + oh + outerMargin
        else:
            y = oy - outerMargin - h
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
        if side == Pack.Right:
            nx = max([(n.x + n.width) for n in neighbors] + [x+w])
            goal = pw - self.parent.innerMargin(Pack.Right)
            growby = goal - nx
            w += growby
            for n in neighbors:
                n.x += growby
        elif side == Pack.Left:
            nx = min([n.x for n in neighbors] + [x])
            goal = self.parent.innerMargin(Pack.Left)
            growby = nx - goal
            w += growby
            x -= growby
            for n in neighbors:
                n.x -= growby
        elif side == Pack.Below:
            ny = min([n.y for n in neighbors] + [y])
            goal = self.parent.innerMargin(Pack.Below)
            growby = ny - goal
            h += growby
            y -= growby
            for n in neighbors:
                n.y -= growby
        else:
            raise Exception("Above fill not supported yet")
        self.x, self.y, self.width, self.height = x, y, w, h
    
    #--- Generate
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.setup = "$viewsetup$\n$addtoparent$\n"
        tmpl.initmethod = "initWithFrame:$rect$"
        x, y, w, h = self.x, self.y, self.width, self.height
        x += self.layoutDeltaX
        y += self.layoutDeltaY
        w += self.layoutDeltaW
        h += self.layoutDeltaH
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
            tmpl.addtoparent = self.generateAddToParent()
        return tmpl
    
    def generateAddToParent(self):
        return self.parent.generateAddSubview(self)
    
    def generateAddSubview(self, subview):
        return self.accessor._callMethod('addSubview', subview)
    
    @property
    def rect(self):
        return self.x, self.y, self.width, self.height
