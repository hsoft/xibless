from .base import convertValueToObjc
from .view import View

class Window(View):
    OBJC_CLASS = 'NSWindow'
    
    def __init__(self, width, height, title):
        View.__init__(self, None, width, height)
        self.xProportion = 0.5
        self.yProportion = 0.5
        self.title = title
        self.canClose = True
        self.canResize = True
        self.canMinimize = True
        self.initialFirstResponder = None
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.initmethod = "initWithContentRect:$rect$ styleMask:$style$ backing:NSBackingStoreBuffered defer:NO"
        tmpl.viewsetup = """{
        NSSize _screenSize = [[NSScreen mainScreen] visibleFrame].size;
        NSSize _windowSize = [$varname$ frame].size;
        CGFloat _windowX = (_screenSize.width - _windowSize.width) * $xprop$;
        CGFloat _windowY = (_screenSize.height - _windowSize.height) * $yprop$;
        [$varname$ setFrameOrigin:NSMakePoint(_windowX, _windowY)];
        }
        """
        tmpl.xprop = convertValueToObjc(self.xProportion)
        tmpl.yprop = convertValueToObjc(self.yProportion)
        styleFlags = ["NSTitledWindowMask"]
        if self.canClose:
            styleFlags.append("NSClosableWindowMask")
        if self.canResize:
            styleFlags.append("NSResizableWindowMask")
        if self.canMinimize:
            styleFlags.append("NSMiniaturizableWindowMask")
        tmpl.style = "|".join(styleFlags)
        self.properties['title'] = self.title
        self.properties['releasedWhenClosed'] = False
        self.properties['initialFirstResponder'] = self.initialFirstResponder
        # Windows don't have autoresizingMask and because it's set in View, we have to remove it.
        del self.properties['autoresizingMask']
        return tmpl
    
    def generateAddSubview(self, subview):
        return self.accessor.contentView._callMethod('addSubview', subview)
    
    def generateFinalize(self):
        return self.accessor._callMethod('recalculateKeyViewLoop')
    
