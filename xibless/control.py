from collections import namedtuple

from .view import View
from .base import const
from .font import Font, FontFamily, FontSize

ControlHeights = namedtuple('ControlHeights', 'regular small mini')

class Control(View):
    CONTROL_HEIGHTS = ControlHeights(20, 17, 14)
    
    def __init__(self, parent, width, height):
        View.__init__(self, parent, width, height)
        self.font = Font(FontFamily.System, FontSize.RegularControl)
        self.controlSize = const.NSRegularControlSize
    
    @property
    def controlSize(self):
        return self._controlSize
    
    @controlSize.setter
    def controlSize(self, value):
        self._controlSize = value
        if value == const.NSMiniControlSize:
            fontSize = FontSize.MiniControl
            height = self.CONTROL_HEIGHTS.mini
        elif value == const.NSSmallControlSize:
            fontSize = FontSize.SmallControl
            height = self.CONTROL_HEIGHTS.small
        else:
            fontSize = FontSize.RegularControl
            height = self.CONTROL_HEIGHTS.regular
        self.font.fontSize = fontSize
        self.height = height
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['font'] = self.font
        self.properties['cell.controlSize'] = self.controlSize
        return tmpl
    
