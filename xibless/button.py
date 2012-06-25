from .base import const
from .font import Font, FontFamily, FontSize
from .view import View

class Button(View):
    OBJC_CLASS = 'NSButton'
    
    LAYOUT_DELTA_X = -6
    LAYOUT_DELTA_Y = -8
    LAYOUT_DELTA_W = 12
    LAYOUT_DELTA_H = 12
    
    DEFAULT_FONT = Font(FontFamily.System, FontSize.RegularControl)
    
    def __init__(self, parent, title, action=None):
        View.__init__(self, parent, 80, 20)
        self.title = title
        self.action = action
        self.font = self.DEFAULT_FONT
    
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
    
