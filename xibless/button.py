from .base import const
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
        self.properties['title'] = self.title
        self.properties['font'] = self.font
        self.properties['buttonType'] = const.NSMomentaryLightButton
        self.properties['bezelStyle'] = const.NSRoundedBezelStyle
        tmpl.viewsetup = "$linkaction$\n"
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
        return tmpl
    
