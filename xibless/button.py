from .base import GeneratedItem

class NSButton(GeneratedItem):
    def __init__(self, parent, rect, title, action=None):
        GeneratedItem.__init__(self)
        self.parent = parent
        self.rect = rect
        self.title = title
        self.action = action
    
    def generateInit(self):
        tmpl = self.template("""NSButton *%%varname%% = [[NSButton alloc] initWithFrame:NSMakeRect(%%rect%%)];
        [%%varname%% setTitle:@"%%title%%"];
        [%%varname%% setButtonType:NSMomentaryLightButton];
        [%%varname%% setBezelStyle:NSRoundedBezelStyle];
        %%linkaction%%
        %%addtoparent%%
        """)
        tmpl.rect = "%d, %d, %d, %d" % self.rect
        tmpl.title = self.title
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
        tmpl.addtoparent = self.parent.generateAddSubview(self)
        return tmpl.render()
    
