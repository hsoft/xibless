from .view import View

class Window(View):
    OBJC_CLASS = 'NSWindow'
    
    def __init__(self, x, y, width, height, title):
        View.__init__(self, None, width, height)
        self.x = x
        self.y = y
        self.title = title
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.allocinit = """
            NSWindow *$varname$ = [[NSWindow alloc] initWithContentRect:$rect$ styleMask:$style$
                backing:NSBackingStoreBuffered defer:NO];
        """
        tmpl.style = "NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask"
        self.properties['title'] = self.title
        # Windows don't have autoresizingMask and because it's set in View, we have to remove it.
        del self.properties['autoresizingMask']
        return tmpl
    
