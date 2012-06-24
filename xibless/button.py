from .view import View

class Button(View):
    OBJC_CLASS = 'NSButton'
    
    def __init__(self, parent, rect, title, action=None):
        View.__init__(self, parent, rect)
        self.title = title
        self.action = action
        self.font = None
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmplsetup = self.template("""
            [$varname$ setTitle:@"$title$"];
            [$varname$ setButtonType:NSMomentaryLightButton];
            [$varname$ setBezelStyle:NSRoundedBezelStyle];
            $setfont$
            $linkaction$
        """)
        tmplsetup.title = self.title
        if self.font:
            tmplsetup.setfont = "[$varname$ setFont:%s];\n" % self.font.varname
        else:
            tmplsetup.setfont = ''
        if self.action:
            tmplsetup.linkaction = self.action.generate(self.varname)
        else:
            tmplsetup.linkaction = ''
        tmpl.viewsetup = tmplsetup.render()
        return tmpl
    
