from .base import convertValueToObjc
from .types import NLSTR
from .view import View
from .toolbar import Toolbar

class Window(View):
    OBJC_CLASS = 'NSWindow'
    PROPERTIES = View.PROPERTIES + ['title', 'minSize', 'maxSize']
    
    def __init__(self, width, height, title):
        View.__init__(self, None, width, height)
        self.xProportion = 0.5
        self.yProportion = 0.5
        self.title = title
        self.canClose = True
        self.canResize = True
        self.canMinimize = True
        self.initialFirstResponder = None
        self.autosaveName = None
        self.toolbar = None
    
    def createToolbar(self, identifier):
        assert self.toolbar is None
        self.toolbar = Toolbar(identifier)
        return self.toolbar
    
    def dependencies(self):
        return View.dependencies(self) + [self.toolbar]
    
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
        self.properties['releasedWhenClosed'] = False
        self.properties['initialFirstResponder'] = self.initialFirstResponder
        # Windows don't have autoresizingMask and because it's set in View, we have to remove it.
        del self.properties['autoresizingMask']
        return tmpl
    
    def generateAddSubview(self, subview):
        return self.accessor.contentView._callMethod('addSubview', subview)
    
    def generateFinalize(self):
        # We have to set frameAutosaveName at finalize because otherwise, the frame is restored
        # before the layout is done and it messes up everything.
        result = ''
        if self.autosaveName:
            result += self._generateProperties({'frameAutosaveName': NLSTR(self.autosaveName)})
        if self.toolbar:
            result += self._generateProperties({'toolbar': self.toolbar})
        result += '\n' + self.accessor._callMethod('recalculateKeyViewLoop')
        return result
    

class PanelStyle(object):
    Regular = 0
    Utility = 1
    HUD = 2

class Panel(Window):
    OBJC_CLASS = 'NSPanel'
    
    def __init__(self, width, height, title):
        Window.__init__(self, width, height, title)
        self.style = PanelStyle.Regular
    
    def generateInit(self):
        tmpl = Window.generateInit(self)
        if self.style == PanelStyle.Utility:
            tmpl.style += '|NSUtilityWindowMask'
        elif self.style == PanelStyle.HUD:
            tmpl.style += '|NSHUDWindowMask'
        return tmpl
    
