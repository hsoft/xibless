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
        self.action = None
    
    def hasFixedHeight(self):
        return True
    
    def _getControlHeights(self):
        return self.CONTROL_HEIGHTS
    
    def _getControlFontSize(self, controlSize):
        if controlSize == const.NSMiniControlSize:
            return FontSize.MiniControl
        elif controlSize == const.NSSmallControlSize:
            return FontSize.SmallControl
        else:
            return FontSize.RegularControl
    
    def _updateLayoutDeltas(self):
        pass
    
    def _updateControlSize(self):
        controlSize = self._controlSize
        controlHeights = self._getControlHeights()
        if controlSize == const.NSMiniControlSize:
            self.height = controlHeights.mini
        elif controlSize == const.NSSmallControlSize:
            self.height = self.CONTROL_HEIGHTS.small
        else:
            self.height = self.CONTROL_HEIGHTS.regular
        self.font.size = self._getControlFontSize(controlSize)
        self._updateLayoutDeltas()
    
    @property
    def controlSize(self):
        return self._controlSize
    
    @controlSize.setter
    def controlSize(self, value):
        self._controlSize = value
        self._updateControlSize()
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['font'] = self.font
        self.properties['cell.controlSize'] = self.controlSize
        if self.action:
            tmpl.setup += self.action.generate(self.varname)
        return tmpl
    
