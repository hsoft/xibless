from .base import GeneratedItem, NSApp, const, convertValueToObjc
from .types import Action
from .property import ImageProperty, ActionProperty, KeyShortcutProperty

class MenuItem(GeneratedItem):
    OBJC_CLASS = 'NSMenuItem'
    PROPERTIES = GeneratedItem.PROPERTIES + [
        'tag', 'hidden', ImageProperty('image'), ActionProperty('action'),
        KeyShortcutProperty('shortcut'), 'state'
    ]
    
    def __init__(self, name, action=None, shortcut=None, tag=None):
        GeneratedItem.__init__(self)
        self.name = name
        self.action = action
        self.shortcut = shortcut
        self.tag = tag
    
    def generateInit(self, menuname):
        tmpl = GeneratedItem.generateInit(self)
        if self.name == "-":
            tmpl.allocinit = "[$menuname$ addItem:[NSMenuItem separatorItem]];\n"
        else:
            tmpl.allocinit = "NSMenuItem *$varname$ = [$menuname$ addItemWithTitle:$name$ action:nil keyEquivalent:@\"\"];"
        tmpl.name = convertValueToObjc(self.name)
        tmpl.menuname = menuname
        return tmpl
    

class Menu(GeneratedItem):
    OBJC_CLASS = 'NSMenu'
    
    def __init__(self, name):
        GeneratedItem.__init__(self)
        self.name = name
        self.items = []
    
    def add(self, menu_or_item, index=None):
        if index is None:
            index = len(self.items)
        self.items.insert(index, menu_or_item)
    
    def addItem(self, name, action=None, shortcut=None, tag=None, index=None):
        item = MenuItem(name, action, shortcut, tag)
        self.add(item, index)
        return item
    
    def addSeparator(self, index=None):
        return self.addItem("-", index=index)
    
    def addMenu(self, name, index=None):
        menu = Menu(name)
        self.add(menu, index)
        return menu
    
    def removeItem(self, index):
        del self.items[index]
    
    def generateInit(self, menuname=None):
        tmpl = GeneratedItem.generateInit(self)
        if menuname:
            tmpl.allocinit = """
                NSMenuItem *_tmpitem = [$menuname$ addItemWithTitle:$name$ action:nil keyEquivalent:@""];
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:$name$] autorelease];
                [$menuname$ setSubmenu:$varname$ forItem:_tmpitem];
            """
        else:
            tmpl.allocinit = """
                NSMenu *$varname$ = [[[NSMenu alloc] initWithTitle:$name$] autorelease];
            """
        tmpl.name = convertValueToObjc(self.name)
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
    

class MainMenu(Menu):
    def __init__(self, appname):
        Menu.__init__(self, "Apple")
        fileMenu = self.addMenu("File")
        editMenu = self.addMenu("Edit")
        windowMenu = self.addMenu("Window")
        helpMenu = self.addMenu("Help")

        fileMenu.addItem("About %s" % appname)
        fileMenu.addSeparator()
        NSApp.servicesMenu = fileMenu.addMenu("Services")
        fileMenu.addSeparator()
        fileMenu.addItem("Hide %s" % appname, Action(NSApp, 'hide:'), 'cmd+h')
        fileMenu.addItem("Hide Others", Action(NSApp, 'hideOtherApplications:'), 'cmd+alt+h')
        fileMenu.addItem("Hide Others", Action(NSApp, 'unhideAllApplications:'))
        fileMenu.addSeparator()
        fileMenu.addItem("Quit %s" % appname, Action(NSApp, 'terminate:'), 'cmd+q')

        editMenu.addItem("Undo", Action(None, 'undo:'), 'cmd+z')
        editMenu.addItem("Redo", Action(None, 'redo:'), 'cmd+shift+z')
        editMenu.addSeparator()
        editMenu.addItem("Cut", Action(None, 'cut:'), 'cmd+x')
        editMenu.addItem("Copy", Action(None, 'copy:'), 'cmd+c')
        editMenu.addItem("Paste", Action(None, 'paste:'), 'cmd+v')
        editMenu.addItem("Paste And Match Style", Action(None, 'pasteAsPlainText:'), 'cmd+alt+shift+v')
        editMenu.addItem("Delete", Action(None, 'delete:'))
        editMenu.addItem("Select All", Action(None, 'selectAll:'), 'cmd+a')
        editMenu.addSeparator()
        findMenu = editMenu.addMenu("Find")
        findMenu.addItem("Find...", Action(None, 'performFindPanelAction:'), 'cmd+f', tag=const.NSFindPanelActionShowFindPanel)
        findMenu.addItem("Find Next", Action(None, 'performFindPanelAction:'), 'cmd+g', tag=const.NSFindPanelActionNext)
        findMenu.addItem("Find Previous", Action(None, 'performFindPanelAction:'), 'cmd+shift+g', tag=const.NSFindPanelActionPrevious)
        findMenu.addItem("Use Selection for Find", Action(None, 'performFindPanelAction:'), 'cmd+e', tag=const.NSFindPanelActionSetFindString)
        findMenu.addItem("Jump to Selection", Action(None, 'centerSelectionInVisibleArea:'), 'cmd+j')
        spellingMenu = editMenu.addMenu("Spelling")
        spellingMenu.addItem("Spelling...", Action(None, 'showGuessPanel:'), 'cmd+:')
        spellingMenu.addItem("Check Spelling", Action(None, 'checkSpelling:'), 'cmd+;')
        spellingMenu.addItem("Check Spelling as You Type", Action(None, 'toggleContinuousSpellChecking:'))

        windowMenu.addItem("Minimize", Action(None, 'performMinimize:'), 'cmd+m')
        windowMenu.addItem("Zoom", Action(None, 'performZoom:'))
        windowMenu.addSeparator()
        windowMenu.addItem("Bring All to Front", Action(None, 'arrangeInFront:'))

        helpMenu.addItem("%s Help" % appname, Action(NSApp, 'showHelp:'), 'cmd+?')
        
        self.fileMenu = fileMenu
        self.editMenu = editMenu
        self.windowMenu = windowMenu
        self.helpMenu = helpMenu
    
