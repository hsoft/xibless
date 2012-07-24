from .view import View, Pack

# The Layout is a **fake** view and generated item. The only reason it's a View subclass is because
# it needs to override layout methods. Eventually, what should happen is that a new base LayoutItem
# base class emerges and that View becomes a subclass of that.

class Layout(View):
    INNER_MARGIN_LEFT = 0 
    INNER_MARGIN_RIGHT = 0
    INNER_MARGIN_ABOVE = 0
    INNER_MARGIN_BELOW = 0
    
    def __init__(self, subviews, filler):
        if len(subviews) < 2:
            raise ValueError("Layouts must have a least two subviews")
        if filler is not None and filler not in subviews:
            raise ValueError("The filler view must be a part of the layout")
        if None in subviews:
            raise ValueError("There can be at most one None element in the layout, and it can't be present at the same time as a filler")
        parent = subviews[0].parent
        View.__init__(self, parent, 1, 1)
        self.subviews = subviews
        self.filler = filler
        self.packToCorner(Pack.UpperLeft)
    
    def _arrangeLayout(self):
        pass
    
    def _updatePos(self):
        self._arrangeLayout()
    
    def isOrHas(self, viewtype, side):
        if side == Pack.Right:
            viewFilter = lambda v: v.x + v.width == self.x + self.width
        elif side == Pack.Left:
            viewFilter = lambda v: v.x == self.x
        elif side == Pack.Above:
            viewFilter = lambda v: v.y + v.height == self.y + self.height
        elif side == Pack.Below:
            viewFilter = lambda v: v.y == self.y
        admissibleViews = filter(viewFilter, self.subviews)
        return any(v.isOrHas(viewtype, side) for v in admissibleViews)
    
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
        Layout.__init__(self, subviews, filler)
        if height:
            self.height = height
        else:
            self.height = max(view.height for view in subviews)
        last = self.subviews[-1]
        self.width = last.x + last.width - self.x
    
    def _arrangeLayout(self):
        if self.left:
            first = self.left[0]
            first.y = self.y
            first.x = self.x
            previous = first
            for view in self.left[1:]:
                view.packRelativeTo(previous, Pack.Right)
                previous = view
        if self.right:
            first = self.right[-1]
            first.y = self.y
            first.x = self.x + self.width - first.width
            previous = first
            for view in reversed(self.right[:-1]):
                view.packRelativeTo(previous, Pack.Left)
                previous = view
        for view in self.subviews:
            if not view.hasFixedHeight():
                view.height = self.height
        if self.filler is not None:
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
        Layout.__init__(self, subviews, filler)
        if width:
            self.width = width
        else:
            self.width = max(view.width for view in subviews)
        first = self.subviews[0]
        self.height = first.y + first.height - self.y
    
    def _arrangeLayout(self):
        if self.above:
            first = self.above[0]
            first.y = self.y + self.height - first.height
            first.x = self.x
            previous = first
            for view in self.above[1:]:
                view.packRelativeTo(previous, Pack.Below)
                previous = view
        if self.below:
            first = self.below[-1]
            first.y = self.y
            first.x = self.x
            previous = first
            for view in reversed(self.below[:-1]):
                view.packRelativeTo(previous, Pack.Above)
                previous = view
        for view in self.subviews:
            if not view.hasFixedWidth():
                view.width = self.width
        if self.filler is not None:
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
    
