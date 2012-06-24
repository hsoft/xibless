from .base import GeneratedItem, KeyShortcut

class MenuItem(GeneratedItem):
    OBJC_CLASS = 'NSMenuItem'
    
    def __init__(self, name, action=None, shortcut=None, tag=None):
        GeneratedItem.__init__(self)
        self.name = name
        self.action = action
        if shortcut and not isinstance(shortcut, KeyShortcut):
            shortcut = KeyShortcut(shortcut)
        self.shortcut = shortcut
        self.tag = tag
    
    def generateInit(self, menuname):
        if self.name == "-":
            tmpl = self.template("[$menuname$ addItem:[NSMenuItem separatorItem]];\n")
        else:
            tmpl = self.template("""
                NSMenuItem *$varname$ = [$menuname$ addItemWithTitle:@"$name$" action:nil keyEquivalent:@"$key$"];
                $linkaction$
                $setkeymask$
                $settag$
            """)
        tmpl.name = self.name
        tmpl.menuname = menuname
        tmpl.settarget = tmpl.setkeymask = tmpl.settag = ""
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
        if self.shortcut:
            tmpl.key = self.shortcut.key
            if self.shortcut.flags:
                tmpl.setkeymask = "[$varname$ setKeyEquivalentModifierMask:%s];" % self.shortcut.flags
        else:
            tmpl.key = "nil"
        if self.tag is not None:
            tag = self.tag._objcAccessor()
            tmpl.settag = "[$varname$ setTag:%s];" % tag
        return tmpl
    

class Menu(MenuItem):
    OBJC_CLASS = 'NSMenu'
    
    def __init__(self, name):
        MenuItem.__init__(self, name, None, None)
        self.items = []
    
    def add(self, menu_or_item):
        self.items.append(menu_or_item)
    
    def addItem(self, *args, **kwargs):
        item = MenuItem(*args, **kwargs)
        self.add(item)
        return item
    
    def addSeparator(self):
        return self.addItem("-")
    
    def addMenu(self, *args, **kwargs):
        menu = Menu(*args, **kwargs)
        self.add(menu)
        return menu
    
    def generateInit(self, menuname=None):
        if menuname:
            tmpl = self.template("""
                NSMenuItem *_tmpitem = [$menuname$ addItemWithTitle:@"$name$" action:nil keyEquivalent:@""];
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:@"$name$"] autorelease];
                [$menuname$ setSubmenu:$varname$ forItem:_tmpitem];
                $subitemscode$
            """)
        else:
            tmpl = self.template("""
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:@"$name$"] autorelease];
                $subitemscode$
            """)
        tmpl.name = self.name
        tmpl.menuname = menuname
        subitemscode = []
        for item in self.items:
            assert isinstance(item, MenuItem)
            item.varname = self.varname + '_sub'
            code = item.generate(self.varname)
            # We wrap it in a block to avoid naming clashes.
            subitemscode.append('{' + code + '}')
        tmpl.subitemscode = '\n'.join(subitemscode)
        return tmpl
    
