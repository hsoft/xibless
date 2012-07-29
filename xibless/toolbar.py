from .base import GeneratedItem, const, convertValueToObjc
from .types import NonLocalizableString
from .view import Size

class Toolbar(GeneratedItem):
    OBJC_CLASS = 'NSToolbar'
    PROPERTIES = GeneratedItem.PROPERTIES + [
        'allowsUserCustomization', 'autosavesConfiguration', 'displayMode',
    ]
    
    def __init__(self, identifier):
        GeneratedItem.__init__(self)
        self.identifier = identifier
        self.items = []
        self.defaultItems = []
        self.allowsUserCustomization = True
    
    def addItem(self, identifier, label, image=None):
        item = ToolbarItem(self, identifier, label, image)
        self.items.append(item)
        return item
    
    def flexibleSpace(self):
        return const.NSToolbarFlexibleSpaceItemIdentifier
    
    def space(self):
        return const.NSToolbarSpaceItemIdentifier
    
    def separator(self):
        return const.NSToolbarSeparatorItemIdentifier
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.initmethod = "initWithIdentifier:$identifier$"
        tmpl.identifier = convertValueToObjc(NonLocalizableString(self.identifier))
        tmpl.setup += "XiblessToolbarDelegate *$varname$Delegate = [[XiblessToolbarDelegate alloc] init]; [$varname$ setDelegate:$varname$Delegate];\n"
        for item in self.items:
            tmpl.setup += item.generate()
            tmpl.setup += "[$varname$Delegate addItem:{}];\n".format(item.varname)
        if self.defaultItems:
            convert = lambda it: convertValueToObjc((NonLocalizableString(it.identifier) if isinstance(it, ToolbarItem) else it))
            defaultItems = ','.join(convert(item) for item in self.defaultItems)
            tmpl.setup += "[$varname$Delegate setDefaultItems:[NSArray arrayWithObjects:{},nil]];\n".format(defaultItems)
        return tmpl
    

class ToolbarItem(GeneratedItem):
    OBJC_CLASS = 'NSToolbarItem'
    PROPERTIES = GeneratedItem.PROPERTIES + ['label', 'paletteLabel', 'view', 'minSize', 'maxSize']
    
    def __init__(self, toolbar, identifier, label, image=None):
        GeneratedItem.__init__(self)
        self.toolbar = toolbar
        self.identifier = toolbar.identifier + identifier
        self.label = label
        self.paletteLabel = label
        self.image = image
        self.view = None
        self.minSize = None
        self.maxSize = None
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        if self.view is not None:
            x, y, w, h = self.view.frameRect()
            if self.minSize is None:
                self.minSize = Size(w, h)
            if self.maxSize is None:
                self.maxSize = Size(w, h)
        tmpl.initmethod = "initWithItemIdentifier:$identifier$"
        tmpl.identifier = convertValueToObjc(NonLocalizableString(self.identifier))
        return tmpl
    
