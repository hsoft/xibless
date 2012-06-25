from .view import View

class Window(View):
    OBJC_CLASS = 'NSWindow'
    
    def __init__(self, rect, title):
        View.__init__(self, None, rect)
        self.title = title
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.allocinit = """
            NSWindow *$varname$ = [[NSWindow alloc] initWithContentRect:$rect$ styleMask:$style$
                backing:NSBackingStoreBuffered defer:NO];
        """
        tmpl.style = "NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask"
        self.properties['title'] = self.title
        return tmpl
    
