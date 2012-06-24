from .view import View

class Label(View):
    OBJC_CLASS = 'NSTextField'
    
    def __init__(self, parent, rect, text):
        View.__init__(self, parent, rect)
        self.text = text
        self.font = None
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        tmplsetup = self.template("""
            [$varname$ setStringValue:@"$text$"];
            [$varname$ setEditable:NO];
            [$varname$ setSelectable:NO];
            [$varname$ setDrawsBackground:NO];
            [$varname$ setBordered:NO];
            $setfont$
        """)
        tmplsetup.text = self.text
        if self.font:
            tmplsetup.setfont = "[$varname$ setFont:%s];\n" % self.font.varname
        else:
            tmplsetup.setfont = ''
        tmpl.viewsetup = tmplsetup.render()
        return tmpl
    
