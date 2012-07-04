from .view import View

class Window(View):
    OBJC_CLASS = 'NSWindow'
    
    def __init__(self, x, y, width, height, title):
        View.__init__(self, None, width, height)
        self.x = x
        self.y = y
        self.title = title
        self.canClose = True
        self.canResize = True
        self.canMinimize = True
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.initmethod = "initWithContentRect:$rect$ styleMask:$style$ backing:NSBackingStoreBuffered defer:NO"
        styleFlags = ["NSTitledWindowMask"]
        if self.canClose:
            styleFlags.append("NSClosableWindowMask")
        if self.canResize:
            styleFlags.append("NSResizableWindowMask")
        if self.canMinimize:
            styleFlags.append("NSMiniaturizableWindowMask")
        tmpl.style = "|".join(styleFlags)
        self.properties['title'] = self.title
        # Windows don't have autoresizingMask and because it's set in View, we have to remove it.
        del self.properties['autoresizingMask']
        return tmpl
    
    def generateAddSubview(self, subview):
        return "[[%s contentView] addSubview:%s];\n" % (self.varname, subview.varname)
    
