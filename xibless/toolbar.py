from .base import GeneratedItem, const, convertValueToObjc, NonLocalizableString
from .view import Size

TOOLBAR_DELEGATE_CODE = """
@interface XiblessToolbarDelegate : NSObject <NSToolbarDelegate>
{
    NSMutableDictionary *items;
    NSArray *defaultItems;
}

- (void)addItem:(NSToolbarItem *)aItem;
- (void)setDefaultItems:(NSArray *)aDefaultItems;
@end

@implementation XiblessToolbarDelegate
- (id)init
{
    self = [super init];
    items = [[NSMutableDictionary alloc] init];
    defaultItems = nil;
    return self;
}

- (void)dealloc
{
    [items release];
    [defaultItems release];
    [super dealloc];
}

- (void)addItem:(NSToolbarItem *)aItem
{
    [items setObject:aItem forKey:[aItem itemIdentifier]];
}

- (void)setDefaultItems:(NSArray *)aDefaultItems
{
    [defaultItems release];
    defaultItems = [aDefaultItems retain];
}

- (NSToolbarItem *)toolbar:(NSToolbar *)toolbar itemForItemIdentifier:(NSString *)itemIdentifier willBeInsertedIntoToolbar:(BOOL)flag
{
    return [items objectForKey:itemIdentifier];
}

- (NSArray *)toolbarAllowedItemIdentifiers:(NSToolbar *)toolbar
{
    NSMutableArray *result = [NSMutableArray array];
    [result addObject:NSToolbarSeparatorItemIdentifier];
    [result addObject:NSToolbarSpaceItemIdentifier];
    [result addObject:NSToolbarFlexibleSpaceItemIdentifier];
    [result addObjectsFromArray:[items allKeys]];
    return result;
}

- (NSArray *)toolbarDefaultItemIdentifiers:(NSToolbar *)toolbar
{
    return defaultItems;
}
@end
"""


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
    
    @classmethod
    def generateSupportCode(cls):
        return TOOLBAR_DELEGATE_CODE
    

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
    
