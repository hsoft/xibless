from .base import GeneratedItem

class Label(GeneratedItem):
    OBJC_CLASS = 'NSTextField'
    
    def __init__(self, parent, rect, text):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
        self.text = text
        self.font = None
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = self.template("""NSTextField *%%varname%% = [[NSTextField alloc] initWithFrame:NSMakeRect(%%rect%%)];
        [%%varname%% setStringValue:@"%%text%%"];
        [%%varname%% setEditable:NO];
        [%%varname%% setSelectable:NO];
        [%%varname%% setDrawsBackground:NO];
        [%%varname%% setBordered:NO];
        %%setfont%%
        %%addtoparent%%
        """)
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.text = self.text
        if self.font:
            tmpl.setfont = "[%s setFont:%s];\n" % (self.varname, self.font.varname)
        else:
            tmpl.setfont = ''
        tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl.render()
    
