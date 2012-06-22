from .base import GeneratedItem, tmpl_replace

class NSWindow(GeneratedItem):
    def __init__(self, rect, title):
        self.rect = rect
        self.title = title
    
    def generateInit(self, varname):
        tmpl = """NSWindow *%%varname%% = [[NSWindow alloc] initWithContentRect:NSMakeRect(%%rect%%)
            styleMask:%%style%% backing:NSBackingStoreBuffered defer:NO];
        [%%varname%% setTitle:@"%%title%%"];
        """
        rect = "%d, %d, %d, %d" % self.rect
        style = "NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask"
        title = self.title
        return tmpl_replace(**vars())
    
