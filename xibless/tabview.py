from .base import GeneratedItem, convertValueToObjc, const
from .view import View, Pack

# Views in tab items have different margins than normal views.
class TabSubView(View):
    INNER_MARGIN_LEFT = 17
    INNER_MARGIN_RIGHT = 17
    INNER_MARGIN_ABOVE = 3
    INNER_MARGIN_BELOW = 17

class TabViewItem(GeneratedItem):
    OBJC_CLASS = 'NSTabViewItem'
    
    def __init__(self, tabview, label, identifier=None):
        GeneratedItem.__init__(self)
        self.label = label
        self._view = TabSubView(None, tabview.width - tabview.OVERHEAD_W,
            tabview.height - tabview.OVERHEAD_H)
        self.identifier = identifier
    
    @property
    def view(self):
        return self._view
    
    def dependencies(self):
        return [self.view] + self.view.subviews
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.initmethod = "initWithIdentifier:$identifier$"
        tmpl.identifier = convertValueToObjc(self.identifier)
        self.properties['label'] = self.label
        self.properties['view'] = self.view
        return tmpl

class TabView(View):
    OBJC_CLASS = 'NSTabView'
    PROPERTIES = View.PROPERTIES + ['tabViewType']
    OVERHEAD_W = 6
    OVERHEAD_H = 30
    
    def __init__(self, parent):
        View.__init__(self, parent, 160, 110)
        self.tabs = []
        self._tabViewType = const.NSTopTabsBezelBorder
        self._updateLayoutDeltas()
    
    def _updatePos(self):
        for tab in self.tabs:
            tab.view.width = self.width - self.OVERHEAD_W
            tab.view.height = self.height - self.OVERHEAD_H
    
    def _updateLayoutDeltas(self):
        if self.tabViewType == const.NSNoTabsNoBorder:
            self.layoutDeltaX = 0
            self.layoutDeltaY = 0
            self.layoutDeltaW = 0
            self.layoutDeltaH = 0
        else:
            self.layoutDeltaX = -7
            self.layoutDeltaY = -10
            self.layoutDeltaW = 14
            self.layoutDeltaH = 16
        
    def innerMarginDelta(self, side):
        if side == Pack.Above:
            return -12
        else:
            return View.innerMarginDelta(self, side)
    
    def addTab(self, label, identifier=None):
        tab = TabViewItem(self, label, identifier)
        self.tabs.append(tab)
        return tab
    
    @property
    def tabViewType(self):
        return self._tabViewType
    
    @tabViewType.setter
    def tabViewType(self, value):
        self._tabViewType = value
        self._updateLayoutDeltas()
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        viewsetup = ""
        for tab in self.tabs:
            tabcode = tab.generate()
            tabcode += "[$varname$ addTabViewItem:%s];\n" % tab.varname
            viewsetup += tabcode
        tmpl.viewsetup = viewsetup
        return tmpl
    
