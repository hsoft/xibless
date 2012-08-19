from .view import View, Pack

# The Layout is a **fake** view and generated item. The only reason it's a View subclass is because
# it needs to override layout methods. Eventually, what should happen is that a new base LayoutItem
# base class emerges and that View becomes a subclass of that.

class Layout(View):
    INNER_MARGIN_LEFT = 0 
    INNER_MARGIN_RIGHT = 0
    INNER_MARGIN_ABOVE = 0
    INNER_MARGIN_BELOW = 0
    
    def __init__(self, subviews, filler, width=0, height=0):
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
        self.moveTo(Pack.UpperLeft)
    
    def _arrangeLayout(self):
        pass
    
    def _updatePos(self):
        self._arrangeLayout()
    
    def isOrHas(self, viewtype, side, strict=False):
        if side == Pack.Right:
            viewFilter = lambda v: v.x + v.width == self.x + self.width
        elif side == Pack.Left:
            viewFilter = lambda v: v.x == self.x
        elif side == Pack.Above:
            viewFilter = lambda v: v.y + v.height == self.y + self.height
        elif side == Pack.Below:
            viewFilter = lambda v: v.y == self.y
        admissibleViews = filter(viewFilter, self.subviews)
        return any(v.isOrHas(viewtype, side, strict=strict) for v in admissibleViews)
    
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
    def __init__(self, subviews, filler=None, height=None):
        left, right = splitByElement(subviews, filler)
        if filler is not None:
            left.append(filler)
            filler.setAnchor(Pack.UpperLeft, growX=True)
        subviews = left + right
        self.left = left
        self.right = right
        if not height:
            height = max(view.height for view in subviews)
        Layout.__init__(self, subviews, filler, height=height)
        maxx = max(v.x+v.width for v in self.subviews)
        minx = min(v.x for v in self.subviews)
        self.width = maxx - minx
    
    def _arrangeLayout(self):
        if self.left:
            first = self.left[0]
            first.y = self.y
            first.x = self.x
            first._updatePos()
            previous = first
            for view in self.left[1:]:
                view.moveNextTo(previous, Pack.Right)
                previous = view
        if self.right:
            first = self.right[-1]
            first.y = self.y
            first.x = self.x + self.width - first.width
            first._updatePos()
            previous = first
            for view in reversed(self.right[:-1]):
                view.moveNextTo(previous, Pack.Left)
                previous = view
        if not self.width:
            # We haven't set a width for our layout yet, so we're in the middle of its
            # initialization. Let's not do anything based on width.
            return
        for view in self.subviews:
            if not view.hasFixedHeight():
                view.height = self.height
                view._updatePos()
        if self.filler is not None:
            if self.right:
                justRight = self.right[0]
                fillGoal = justRight.x - self._getOuterMargin(justRight, Pack.Right)
            else:
                fillGoal = self.x + self.width
            self.filler.fill(Pack.Right, goal=fillGoal)
    
    def setAnchor(self, side):
        if side == Pack.Above:
            leftAnchor = Pack.UpperLeft
            rightAnchor = Pack.UpperRight
        else:
            leftAnchor = Pack.LowerLeft
            rightAnchor = Pack.LowerRight
        for view in self.left:
            view.setAnchor(leftAnchor)
        for view in self.right:
            view.setAnchor(rightAnchor)
        if self.filler is not None:
            self.filler.setAnchor(leftAnchor, growX=True)
    
    
class VLayout(Layout):
    def __init__(self, subviews, filler=None, width=None):
        above, below = splitByElement(subviews, filler)
        if filler is not None:
            above.append(filler)
            filler.setAnchor(Pack.UpperLeft, growY=True)
        subviews = above + below
        self.above = above
        self.below = below
        if not width:
            width = max(view.width for view in subviews)
        Layout.__init__(self, subviews, filler, width=width)
        maxy = max(v.y+v.height for v in self.subviews)
        miny = min(v.y for v in self.subviews)
        self.height = maxy - miny
    
    def _arrangeLayout(self):
        if self.above:
            first = self.above[0]
            first.y = self.y + self.height - first.height
            first.x = self.x
            first._updatePos()
            previous = first
            for view in self.above[1:]:
                view.moveNextTo(previous, Pack.Below)
                previous = view
        if self.below:
            first = self.below[-1]
            first.y = self.y
            first.x = self.x
            first._updatePos()
            previous = first
            for view in reversed(self.below[:-1]):
                view.moveNextTo(previous, Pack.Above)
                previous = view
        if not self.height:
            # See HLayout._arrangeLayout()
            return
        for view in self.subviews:
            if not view.hasFixedWidth():
                view.width = self.width
                view._updatePos()
        if self.filler is not None:
            if self.below:
                justUnder = self.below[0]
                fillGoal = justUnder.y + justUnder.height + self._getOuterMargin(justUnder, Pack.Below)
            else:
                fillGoal = self.y
            self.filler.fill(Pack.Below, goal=fillGoal)
    
    def setAnchor(self, side):
        if side == Pack.Left:
            aboveAnchor = Pack.UpperLeft
            belowAnchor = Pack.LowerLeft
        else:
            aboveAnchor = Pack.UpperRight
            belowAnchor = Pack.LowerRight
        for view in self.above:
            view.setAnchor(aboveAnchor)
        for view in self.below:
            view.setAnchor(belowAnchor)
        if self.filler is not None:
            self.filler.setAnchor(aboveAnchor, growY=True)
    

class VHLayout(VLayout):
    def __init__(self, viewGrid, fillers=None, width=None):
        if fillers is None:
            fillers = set()
        layouts = []
        for views in viewGrid:
            filler = None
            for candidate in fillers:
                if candidate in views:
                    filler = candidate
                    break
            layouts.append(HLayout(views, filler))
        VLayout.__init__(self, layouts, width=width)
