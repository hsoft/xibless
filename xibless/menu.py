from .base import GeneratedItem, KeyShortcut, tmpl_replace

class NSMenuItem(GeneratedItem):
    def __init__(self, name, action=None, shortcut=None, tag=None):
        GeneratedItem.__init__(self)
        self.name = name
        self.action = action
        if shortcut and not isinstance(shortcut, KeyShortcut):
            shortcut = KeyShortcut(shortcut)
        self.shortcut = shortcut
        self.tag = tag
    
    def generateInit(self, varname, menuname):
        if self.name == "-":
            tmpl = "[%%menuname%% addItem:[NSMenuItem separatorItem]];\n"
        else:
            tmpl = """NSMenuItem *%%varname%% = [%%menuname%% addItemWithTitle:@"%%name%%" action:%%action%% keyEquivalent:@"%%key%%"];
            %%settarget%%
            %%setkeymask%%
            %%settag%%
            """
        name = self.name
        settarget = setkeymask = settag = ""
        if self.action:
            action = "@selector(%s)" % self.action.selector
            if self.action.target:
                target = self.action.target._objcAccessor()
            else:
                target = 'nil'
            settarget = "[%s setTarget:%s];" % (varname, target)
        else:
            action = "nil"
        if self.shortcut:
            key = self.shortcut.key
            if self.shortcut.flags:
                setkeymask = "[%s setKeyEquivalentModifierMask:%s];" % (varname, self.shortcut.flags)
        else:
            key = "nil"
        if self.tag is not None:
            tag = self.tag._objcAccessor()
            settag = "[%s setTag:%s];" % (varname, tag)
        return tmpl_replace(**vars())
    

class NSMenu(NSMenuItem):
    def __init__(self, name):
        NSMenuItem.__init__(self, name, None, None)
        self.items = []
    
    def add(self, menu_or_item):
        self.items.append(menu_or_item)
    
    def addItem(self, *args, **kwargs):
        item = NSMenuItem(*args, **kwargs)
        self.add(item)
        return item
    
    def addSeparator(self):
        return self.addItem("-")
    
    def addMenu(self, *args, **kwargs):
        menu = NSMenu(*args, **kwargs)
        self.add(menu)
        return menu
    
    def generateInit(self, varname, menuname=None):
        if menuname:
            tmpl = """NSMenuItem *_tmpitem = [%%menuname%% addItemWithTitle:@"%%name%%" action:nil keyEquivalent:@""];
            NSMenu *%%varname%% = [[[NSMenu alloc] initWithTitle:@"%%name%%"] autorelease];
            [%%menuname%% setSubmenu:%%varname%% forItem:_tmpitem];
            %%subitemscode%%
            """
        else:
            tmpl = """NSMenu *%%varname%% = [[[NSMenu alloc] initWithTitle:@"%%name%%"] autorelease];
            %%subitemscode%%
            """
        name = self.name
        subitemscode = []
        for item in self.items:
            assert isinstance(item, NSMenuItem)
            code = item.generate(varname+'_sub', varname)
            # We wrap it in a block to avoid naming clashes.
            subitemscode.append('{' + code + '}')
        subitemscode = '\n'.join(subitemscode)
        return tmpl_replace(**vars())
    
