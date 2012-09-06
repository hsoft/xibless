from collections import namedtuple

from .view import View
from .base import const
from .property import Property, ActionProperty
from .font import Font, FontFamily, FontSize

ControlHeights = namedtuple('ControlHeights', 'regular small mini')

class ControlSize(object):
    Regular = const.NSRegularControlSize
    Small = const.NSSmallControlSize
    Mini = const.NSMiniControlSize

class TextAlignment(object):
    Left = const.NSLeftTextAlignment
    Right = const.NSRightTextAlignment
    Center = const.NSCenterTextAlignment
    Justified = const.NSJustifiedTextAlignment
    Natural = const.NSNaturalTextAlignment
    
class Control(View):
    CONTROL_HEIGHTS = ControlHeights(20, 17, 14)
    PROPERTIES = View.PROPERTIES + [
        ActionProperty('action'), 'font', Property('controlSize', 'cell.controlSize'), 'formatter',
        'alignment'
    ]
    
    def __init__(self, parent, width, height):
        View.__init__(self, parent, width, height)
        self.font = Font(FontFamily.System, FontSize.RegularControl)
        self.controlSize = ControlSize.Regular
        self.action = None
        self.formatter = None
    
    def _hasFixedHeight(self):
        return True
    
    def _getControlHeights(self):
        return self.CONTROL_HEIGHTS
    
    def _getControlFontSize(self, controlSize):
        if controlSize == ControlSize.Mini:
            return FontSize.MiniControl
        elif controlSize == ControlSize.Small:
            return FontSize.SmallControl
        else:
            return FontSize.RegularControl
    
    def _updateLayoutDeltas(self):
        pass
    
    def _updateControlSize(self):
        controlSize = self._controlSize
        controlHeights = self._getControlHeights()
        if controlSize == ControlSize.Mini:
            self.height = controlHeights.mini
        elif controlSize == ControlSize.Small:
            self.height = controlHeights.small
        else:
            self.height = controlHeights.regular
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
        return View.dependencies(self) + [self.font, self.formatter]
    
