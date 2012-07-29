from .base import convertValueToObjc
from .types import KeyValueId
from .view import View
from .font import Font, FontFamily, FontSize

class TextView(View):
    OBJC_CLASS = 'NSTextView'
    
    DEFAULT_FONT = Font(FontFamily.Label, FontSize.RegularControl)
    
    def __init__(self, parent):
        View.__init__(self, parent, 100, 22)
        self.text = ''
        self.font = self.DEFAULT_FONT
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmpl.viewsetup = """NSScrollView *$varname$_container = [[[NSScrollView alloc] initWithFrame:$rect$] autorelease];
            [$varname$_container setDocumentView:$varname$];
            [$varname$_container setHasVerticalScroller:YES];
            [$varname$_container setHasHorizontalScroller:NO];
            [$varname$_container setAutohidesScrollers:NO];
            [$varname$_container setBorderType:NSBezelBorder];
            [$varname$_container setAutoresizingMask:$autoresize$];
        """
        tmpl.autoresize = convertValueToObjc(self.properties['autoresizingMask'])
        self.properties['textStorage.mutableString.string'] = self.text
        self.properties['textStorage.font'] = self.font
        return tmpl
    
    def generateAddToParent(self):
        container = KeyValueId(None, self.varname + '_container')
        return self.parent.generateAddSubview(container)
    
