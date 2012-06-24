from .base import GeneratedItem

class NSButton(GeneratedItem):
    def __init__(self, parent, rect, title, action=None):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
        self.title = title
        self.action = action
        self.font = None
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = self.template("""NSButton *%%varname%% = [[NSButton alloc] initWithFrame:NSMakeRect(%%rect%%)];
        [%%varname%% setTitle:@"%%title%%"];
        [%%varname%% setButtonType:NSMomentaryLightButton];
        [%%varname%% setBezelStyle:NSRoundedBezelStyle];
        %%setfont%%
        %%linkaction%%
        %%addtoparent%%
        """)
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.title = self.title
        if self.font:
            tmpl.setfont = "[%s setFont:%s];\n" % (self.varname, self.font.varname)
        else:
            tmpl.setfont = ''
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
        tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl.render()
    
