from .view import View, Pack

# The Layout is a **fake** view and generated item. The only reason it's a View subclass is because
# it needs to override layout methods. Eventually, what should happen is that a new base LayoutItem
# base class emerges and that View becomes a subclass of that.

class Layout(View):
    INNER_MARGIN_LEFT = 0 
    INNER_MARGIN_RIGHT = 0
    INNER_MARGIN_ABOVE = 0
    INNER_MARGIN_BELOW = 0
    
    def __init__(self, subviews, filler, width=0, height=0, margin=None):
        if len(subviews) < 2:
            raise ValueError("Layouts must have a least two subviews")
        if filler is not None and filler not in subviews:
            raise ValueError("The filler view must be a part of the layout")
        if None in subviews:
            raise ValueError("There can be at most one None element in the layout, and it can't be present at the same time as a filler")
        parent = subviews[0].parent
        View.__init__(self, parent, width, height)
        self.subviews = subviews
        self.filler = filler
        self.margin = margin
        self.moveTo(Pack.UpperLeft)
    
    def _arrangeLayout(self):
        pass
    
    def _updatePos(self):
        self._arrangeLayout()
    
    def _getInterViewMargin(self, view, other, side):
        if self.margin is not None:
            return self.margin
        else:
            return view._getOuterMargin(other, side)
    
    def viewsAtSide(self, side):
        if side == Pack.Right:
            viewFilter = lambda v: v.x + v.width == self.x + self.width
        elif side == Pack.Left:
            viewFilter = lambda v: v.x == self.x
        elif side == Pack.Above:
            viewFilter = lambda v: v.y + v.height == self.y + self.height
        elif side == Pack.Below:
            viewFilter = lambda v: v.y == self.y
        return list(filter(viewFilter, self.subviews))
    
    def outerMargin(self, other, side):
        return max(view.outerMargin(other, side) for view in self.subviews)
    
    # We don't want to be generating any objc code for the layout.
    def generate(self, *args, **kwargs):
        return ''

def splitByElement(views, element):
    if element not in views:
        return views, []
    index = views.index(element)
    return views[:index], views[index+1:]

class HLayout(Layout):
    def __init__(self, subviews, filler=None, height=None, margin=None, align=None):
        left, right = splitByElement(subviews, filler)
        if filler is not None:
            left.append(filler)
        subviews = left + right
        self.left = left
        self.right = right
        if not height:
            height = max(view.height for view in subviews)
        self.align = align
        Layout.__init__(self, subviews, filler, height=height, margin=margin)
        maxx = max(v.x+v.width for v in self.subviews)
        minx = min(v.x for v in self.subviews)
        self.width = maxx - minx
    
    def _arrangeLayout(self):
        # It's possible to have _arrangeLayout() called with a 0 width, this means that we're in
        # initialization and that we should avoid doing any layout operations that require a width.
        if self.width:
            # We have to set the width of our flexible width widgets before we move them inside
            # their calculated rect or else we will misalign them on the basis of false width.
            for view in self.subviews:
                if not view.hasFixedHeight():
                    view.height = self.height
                    view._updatePos()
        rect = self.rect
        if self.left:
            first = self.left[0]
            rect.width = first.width
            first.moveInsideRect(rect, valign=self.align)
            previous = first
            for view in self.left[1:]:
                margin = self._getInterViewMargin(view, previous, Pack.Right)
                rect.x += rect.width + margin
                rect.width = view.width
                view.moveInsideRect(rect, valign=self.align)
                previous = view
        if self.right:
            first = self.right[-1]
            rect.width = first.width
            rect.x = self.x + self.width - first.width
            first.moveInsideRect(rect, valign=self.align)
            previous = first
            for view in reversed(self.right[:-1]):
                margin = self._getInterViewMargin(view, previous, Pack.Left)
                rect.width = view.width
                rect.x -= rect.width + margin
                view.moveInsideRect(rect, valign=self.align)
                previous = view
        if self.width and self.filler is not None:
            if self.right:
                justRight = self.right[0]
                fillGoal = justRight.x - self._getInterViewMargin(self.filler, justRight, Pack.Left)
            else:
                fillGoal = self.x + self.width
            self.filler.fill(Pack.Right, goal=fillGoal)
    
    def setAnchor(self, side, growY=False):
        if side not in {Pack.Above, Pack.Below}:
            raise ValueError("setAnchor() can only be called with Above or Below in HLayouts.")
        if side == Pack.Above:
            leftAnchor = Pack.UpperLeft
            rightAnchor = Pack.UpperRight
        else:
            leftAnchor = Pack.LowerLeft
            rightAnchor = Pack.LowerRight
        for view in self.left:
            if isinstance(view, VLayout):
                view.setAnchor(Pack.Left)
            else:
                view.setAnchor(leftAnchor, growY=growY)
        for view in self.right:
            if isinstance(view, VLayout):
                view.setAnchor(Pack.Right)
            else:
                view.setAnchor(rightAnchor, growY=growY)
        if self.filler is not None:
            if isinstance(self.filler, VLayout):
                self.filler.setAnchor(Pack.Left, growX=True)
            else:
                self.filler.setAnchor(leftAnchor, growX=True, growY=growY)
    

class VLayout(Layout):
    def __init__(self, subviews, filler=None, width=None, margin=None, align=None):
        above, below = splitByElement(subviews, filler)
        if filler is not None:
            above.append(filler)
        subviews = above + below
        self.above = above
        self.below = below
        if not width:
            width = max(view.width for view in subviews)
        self.align = align
        Layout.__init__(self, subviews, filler, width=width, margin=margin)
        maxy = max(v.y+v.height for v in self.subviews)
        miny = min(v.y for v in self.subviews)
        self.height = maxy - miny
    
    def _arrangeLayout(self):
        # See HLayout._arrangeLayout() comments, they apply here as well.
        if self.height:
            for view in self.subviews:
                if not view.hasFixedWidth():
                    view.width = self.width
                    view._updatePos()
        rect = self.rect
        if self.above:
            first = self.above[0]
            rect.height = first.height
            rect.y = self.y + self.height - first.height
            first.moveInsideRect(rect, halign=self.align)
            previous = first
            for view in self.above[1:]:
                margin = self._getInterViewMargin(view, previous, Pack.Below)
                rect.height = view.height
                rect.y -= rect.height + margin
                view.moveInsideRect(rect, halign=self.align)
                previous = view
        if self.below:
            first = self.below[-1]
            rect.y = self.y
            rect.height = first.height
            first.moveInsideRect(rect, halign=self.align)
            previous = first
            for view in reversed(self.below[:-1]):
                margin = self._getInterViewMargin(view, previous, Pack.Above)
                rect.y += rect.height + margin
                rect.height = view.height
                view.moveInsideRect(rect, halign=self.align)
                previous = view
        if self.height and self.filler is not None:
            if self.below:
                justUnder = self.below[0]
                fillGoal = justUnder.y + justUnder.height + self._getInterViewMargin(self.filler, justUnder, Pack.Above)
            else:
                fillGoal = self.y
            self.filler.fill(Pack.Below, goal=fillGoal)
    
    def setAnchor(self, side, growX=False):
        if side not in {Pack.Left, Pack.Right}:
            raise ValueError("setAnchor() can only be called with Left or Right in VLayouts.")
        if side == Pack.Left:
            aboveAnchor = Pack.UpperLeft
            belowAnchor = Pack.LowerLeft
        else:
            aboveAnchor = Pack.UpperRight
            belowAnchor = Pack.LowerRight
        for view in self.above:
            if isinstance(view, HLayout):
                view.setAnchor(Pack.Above)
            else:
                view.setAnchor(aboveAnchor, growX=growX)
        for view in self.below:
            if isinstance(view, HLayout):
                view.setAnchor(Pack.Below)
            else:
                view.setAnchor(belowAnchor, growX=growX)
        if self.filler is not None:
            if isinstance(self.filler, HLayout):
                self.filler.setAnchor(Pack.Above, growY=True)
            else:
                self.filler.setAnchor(aboveAnchor, growX=growX, growY=True)
    

class VHLayout(VLayout):
    def __init__(self, viewGrid, hfillers=None, vfiller=None, width=None, hmargin=None, vmargin=None,
            halign=None, valign=None):
        if hfillers is None:
            hfillers = set()
        layouts = []
        mainFiller = None
        for views in viewGrid:
            if not views:
                continue
            if len(views) == 1:
                # With only one view, add it directly
                layouts.append(views[0])
                if vfiller is not None and views[0] is vfiller:
                    mainFiller = views[0]
                continue
            filler = None
            for candidate in hfillers:
                if candidate in views:
                    filler = candidate
                    break
            layout = HLayout(views, filler, margin=hmargin, align=valign)
            if vfiller is not None and vfiller in views:
                mainFiller = layout
            layouts.append(layout)
        VLayout.__init__(self, layouts, filler=mainFiller, width=width, margin=vmargin, align=halign)
