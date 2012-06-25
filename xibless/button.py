from .base import const
from .view import View

class Button(View):
    OBJC_CLASS = 'NSButton'
    
    LAYOUT_DELTA_X = -6
    LAYOUT_DELTA_Y = -8
    LAYOUT_DELTA_W = 12
    LAYOUT_DELTA_H = 12
    
    def __init__(self, parent, title, width, height=20, action=None):
        View.__init__(self, parent, width, height)
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
    
