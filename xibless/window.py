from .base import GeneratedItem

class Window(GeneratedItem):
    OBJC_CLASS = 'NSWindow'
    
    def __init__(self, rect, title):
        GeneratedItem.__init__(self)
        self.rect = rect
        self.title = title
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.allocinit = """
            NSWindow *$varname$ = [[NSWindow alloc] initWithContentRect:NSMakeRect($rect$)
                styleMask:$style$ backing:NSBackingStoreBuffered defer:NO];
        """
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.style = "NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask"
        self.properties['title'] = self.title
        return tmpl
    
    def generateAddSubview(self, subview):
        return "[[%s contentView] addSubview:%s];\n" % (self.varname, subview.varname)
    
