from .base import GeneratedItem

class NSWindow(GeneratedItem):
    def __init__(self, rect, title):
        GeneratedItem.__init__(self)
        self.rect = rect
        self.title = title
    
    def generateInit(self):
        tmpl = self.template("""
            NSWindow *%%varname%% = [[NSWindow alloc] initWithContentRect:NSMakeRect(%%rect%%)
                styleMask:%%style%% backing:NSBackingStoreBuffered defer:NO];
            [%%varname%% setTitle:@"%%title%%"];
        """)
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.style = "NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask"
        tmpl.title = self.title
        return tmpl.render()
    
    def generateAddSubview(self, subview):
        tmpl = self.template("[[%%varname%% contentView] addSubview:%%subview%%];\n")
        tmpl.subview = subview.varname
        return tmpl.render()
    
