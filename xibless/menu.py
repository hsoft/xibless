from .base import GeneratedItem, KeyShortcut, Literal

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
        tmpl = GeneratedItem.generateInit(self)
        if self.name == "-":
            tmpl.allocinit = "[$menuname$ addItem:[NSMenuItem separatorItem]];\n"
            tmpl.setup = ""
        else:
            tmpl.allocinit = "NSMenuItem *$varname$ = [$menuname$ addItemWithTitle:@\"$name$\" action:nil keyEquivalent:@\"$key$\"];"
            tmpl.setup = "$linkaction$"
        tmpl.name = self.name
        tmpl.menuname = menuname
        if self.action:
            tmpl.linkaction = self.action.generate(self.varname)
        else:
            tmpl.linkaction = ''
        if self.shortcut:
            tmpl.key = self.shortcut.key
            if self.shortcut.flags:
                self.properties['keyEquivalentModifierMask'] = Literal(self.shortcut.flags)
        else:
            tmpl.key = "nil"
        self.properties['tag'] = self.tag
        return tmpl
    

class Menu(GeneratedItem):
    OBJC_CLASS = 'NSMenu'
    
    def __init__(self, name):
        GeneratedItem.__init__(self)
        self.name = name
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
        tmpl = GeneratedItem.generateInit(self)
        if menuname:
            tmpl.allocinit = """
                NSMenuItem *_tmpitem = [$menuname$ addItemWithTitle:@"$name$" action:nil keyEquivalent:@""];
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:@"$name$"] autorelease];
                [$menuname$ setSubmenu:$varname$ forItem:_tmpitem];
            """
        else:
            tmpl.allocinit = """
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:@"$name$"] autorelease];
            """
        tmpl.name = self.name
        tmpl.menuname = menuname
        subitemscode = []
        for item in self.items:
            assert isinstance(item, (Menu, MenuItem))
            item.varname = self.varname + '_sub'
            code = item.generate(self.varname)
            # We wrap it in a block to avoid naming clashes.
            subitemscode.append('{' + code + '}')
        tmpl.setup = '\n'.join(subitemscode)
        return tmpl
    
