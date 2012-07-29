from __future__ import division

from collections import namedtuple, defaultdict

from .base import GeneratedItem
from .types import Literal

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
    
    @staticmethod
    def isSide(sideOrCorner):
        return sideOrCorner in {Pack.Left, Pack.Right, Pack.Above, Pack.Below, Pack.Middle}
    
    @staticmethod
    def isCorner(sideOrCorner):
        return sideOrCorner in {Pack.UpperLeft, Pack.UpperRight, Pack.LowerLeft, Pack.LowerRight}
    
    @staticmethod
    def sidesInCorner(corner):
        assert Pack.isCorner(corner)
        if corner == Pack.UpperLeft:
            return {Pack.Left, Pack.Above}
        elif corner == Pack.UpperRight:
            return {Pack.Right, Pack.Above}
        elif corner == Pack.LowerRight:
            return {Pack.Right, Pack.Below}
        elif corner == Pack.LowerLeft:
            return {Pack.Left, Pack.Below}

Anchor = namedtuple('Anchor', 'corner growX growY')

class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def objcValue(self):
        return 'NSMakeSize(%d, %d)' % (self.width, self.height)
    

class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def objcValue(self):
        return 'NSMakeRect(%d, %d, %d, %d)' % (self.x, self.y, self.width, self.height)
    

class View(GeneratedItem):
    OBJC_CLASS = 'NSView'
    PROPERTIES = GeneratedItem.PROPERTIES + ['menu']
    
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
    
    def _updatePos(self):
        # This is called after the view had its position changed by a layout method. Here, we do
        # nothing, but the Layout subclass does.
        pass
    
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
    
    def innerMarginDelta(self, side):
        # This is called in pair with innerMargin to the child view for which we need to know where
        # to place inside a view. Most of the time, we just user innerMargin, but some view, like
        # the TabView, are placed closer to the border.
        return 0
    
    # The x, y, width and height pos represent the **layout* rect. To have a frame rect, we need
    # to apply deltas.
    def frameRect(self):
        x, y, w, h = self.x, self.y, self.width, self.height
        x += self.layoutDeltaX
        y += self.layoutDeltaY
        w += self.layoutDeltaW
        h += self.layoutDeltaH
        return x, y, w, h
    
    # Return True if the view can't have its width or height modified by layout methods.
    def hasFixedWidth(self):
        return False
    
    def hasFixedHeight(self):
        return False
    
    def isOrHas(self, viewtype, side):
        # Returns whether self is of type `viewtype` or if it contains a view, touching `side`,
        # that is of that type (Overridden by layouts)
        return isinstance(self, viewtype)
    
    def packToCorner(self, corner, margin=None):
        def getmargin(side):
            if margin is not None:
                return margin
            else:
                result = self.parent.innerMargin(side)
                result += self.innerMarginDelta(side)
                return result
        
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        if corner in (Pack.LowerLeft, Pack.UpperLeft):
            x = getmargin(Pack.Left)
        else:            
            x = pw - self.parent.innerMargin(Pack.Right) - w
        if corner in (Pack.LowerLeft, Pack.LowerRight):
            y = getmargin(Pack.Below)
        else:            
            y = ph - getmargin(Pack.Above) - h
        self.x, self.y = x, y
        self._updatePos()
    
    def packRelativeTo(self, other, side, align=None, margin=None):
        assert other.parent is self.parent
        ox, oy, ow, oh = other.rect
        x, y, w, h = self.rect
        if margin is not None:
            outerMargin = margin
        else:
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
        self._updatePos()
    
    def setAnchor(self, corner, growX=False, growY=False):
        self.anchor = Anchor(corner, growX, growY)
    
    def fill(self, side, margin=None, goal=None):
        def getmargin(side):
            if margin is not None:
                return margin
            else:
                return self.parent.innerMargin(side)
        
        if Pack.isCorner(side):
            for side in Pack.sidesInCorner(side):
                self.fill(side, margin=margin)
            return
        if side in {Pack.Left, Pack.Right} and self.hasFixedWidth():
            return
        if side in {Pack.Above, Pack.Below} and self.hasFixedHeight():
            return        
        assert self.parent is not None
        px, py, pw, ph = self.parent.rect
        x, y, w, h = self.rect
        neighbors = self.neighbors[side]
        if side == Pack.Right:
            nx = max([(n.x + n.width) for n in neighbors] + [x+w])
            if goal is None:
                goal = pw - getmargin(Pack.Right)
            growby = goal - nx
            w += growby
            for n in neighbors:
                n.x += growby
        elif side == Pack.Left:
            nx = min([n.x for n in neighbors] + [x])
            if goal is None:
                goal = getmargin(Pack.Left)
            growby = nx - goal
            w += growby
            x -= growby
            for n in neighbors:
                n.x -= growby
        elif side == Pack.Below:
            ny = min([n.y for n in neighbors] + [y])
            if goal is None:
                goal = getmargin(Pack.Below)
            growby = ny - goal
            h += growby
            y -= growby
            for n in neighbors:
                n.y -= growby
        elif side == Pack.Above:
            ny = max([n.y + n.height for n in neighbors] + [y+h])
            if goal is None:
                goal = ph - getmargin(Pack.Above)
            growby = goal - ny
            h += growby
            for n in neighbors:
                n.y += growby
        else:
            raise ValueError("Wrong side argument")
        self.x, self.y, self.width, self.height = x, y, w, h
        self._updatePos()
        for n in neighbors:
            n._updatePos()
    
    #--- Generate
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.setup = "$viewsetup$\n$addtoparent$\n"
        tmpl.initmethod = "initWithFrame:$rect$"
        x, y, w, h = self.frameRect()
        tmpl.rect = Rect(x, y, w, h).objcValue()
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
