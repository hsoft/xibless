from .view import View

class SplitView(View):
    OBJC_CLASS = 'NSSplitView'
    PROPERTIES = View.PROPERTIES + ['vertical', 'dividerStyle']
    
    def __init__(self, parent, subviewCount, vertical):
        View.__init__(self, parent, 100, 100)
        self.vertical = vertical
        for _ in range(subviewCount):
            # Simply by having `self` as its parent, the view is appended to self.subviews
            View(self, 100, 100)
    
