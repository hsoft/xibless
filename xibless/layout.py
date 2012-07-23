from .view import View, Pack

# The Layout is a **fake** view and generated item. The only reason it's a View subclass is because
# it needs to override layout methods. Eventually, what should happen is that a new base LayoutItem
# base class emerges and that View becomes a subclass of that.

class HLayout(View):
    INNER_MARGIN_LEFT = 0 
    INNER_MARGIN_RIGHT = 0
    INNER_MARGIN_ABOVE = 0
    INNER_MARGIN_BELOW = 0
    
    def __init__(self, left, right):
        if len(left + right) < 2:
            raise ValueError("Layouts must have a least two subviews")
        subviews = left + right
        parent = subviews[0].parent
        View.__init__(self, parent, 1, 1)
        self.left = left
        self.right = right
        self.subviews = subviews
        self._adaptLayoutSize()
        self.setAnchor(Pack.UpperLeft)
        self.packToCorner(Pack.UpperLeft)
        self.fill(Pack.Right)
    
    def _adaptLayoutSize(self):
        self.height = max(view.height for view in self.subviews)
    
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
    
    def _updatePos(self):
        self._arrangeLayout()
    
    def outerMargin(self, other, side):
        if not self.subviews:
            return 0
        return max(view.outerMargin(other, side) for view in self.subviews)
    
    def packToCorner(self, *args, **kwargs):
        self._adaptLayoutSize()
        View.packToCorner(self, *args, **kwargs)
    
    def packRelativeTo(self, *args, **kwargs):
        self._adaptLayoutSize()
        View.packRelativeTo(self, *args, **kwargs)
    
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
    
    def fill(self, *args, **kwargs):
        self._adaptLayoutSize()
        View.fill(self, *args, **kwargs)
    
    # We don't want to be generating any objc code for the layout.
    def generate(self, *args, **kwargs):
        return ''
    
