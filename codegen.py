import os.path
import importlib
from collections import namedtuple

try:
    execfile
except NameError:
    # We're in Python 3
    def execfile(file, globals=globals(), locals=locals()):
        with open(file, "r") as fh:
            exec(fh.read()+"\n", globals, locals)

UNIT_TMPL = """
#import <Cocoa/Cocoa.h>

%%classname%%* create%%name%%(%%ownerclass%% *owner)
{
%%classname%% *result;
%%contents%%
return result;
}
"""

def tmpl_replace(tmpl, **replacements):
    # Because we generate code and that code is likely to contain "{}" braces, it's better if we
    # use more explicit placeholders than the typecal format() method. These placeholders are
    # %%name%%.
    result = tmpl
    for placeholder, replacement in replacements.items():
        wrapped_placeholder = '%%{}%%'.format(placeholder)
        if wrapped_placeholder not in result:
            continue
        result = result.replace(wrapped_placeholder, replacement)
    return result

def generate(module_path, dest):
    module_globals = {
        'NSMenu': NSMenu,
        'Action': Action,
    }
    module_locals = {}
    execfile(module_path, module_globals, module_locals)
    assert 'result' in module_locals
    name = os.path.splitext(os.path.basename(dest))[0]
    result = module_locals['result']
    ownerclass = module_locals.get('ownerclass', 'id')
    classname = result.__class__.__name__
    contents = result.generate('result')
    fp = open(dest, 'wt')
    fp.write(tmpl_replace(UNIT_TMPL, **vars()))
    fp.close()
    
Action = namedtuple('Action', 'target selector')

class KeyShortcut(object):
    def __init__(self, shortcutStr):
        self.shortcutStr = shortcutStr
        elements = set(shortcutStr.lower().split('+'))
        flags = []
        availableFlags = [
            ('cmd', 'NSCommandKeyMask'),
            ('ctrl', 'NSControlKeyMask'),
            ('alt', 'NSAlternateKeyMask'),
            ('shift', 'NSShiftKeyMask'),
        ]
        for ident, flag in availableFlags:
            if ident in elements:
                elements.remove(ident)
                flags.append(flag)
        self.flags = '|'.join(flags)
        assert len(elements) == 1
        self.key = list(elements)[0]
        

class NSMenuItem(object):
    def __init__(self, name, action=None, shortcut=None):
        self.name = name
        self.action = action
        if shortcut and not isinstance(shortcut, KeyShortcut):
            shortcut = KeyShortcut(shortcut)
        self.shortcut = shortcut
    
    def generate(self, varname, menuname):
        tmpl = """NSMenuItem *%%varname%% = [%%menuname%% addItemWithTitle:@"%%name%%" action:%%action%% keyEquivalent:@"%%key%%"];
        %%settarget%%
        %%setkeymask%%
        """
        name = self.name
        if self.action:
            action = "@selector(%s)" % self.action.selector
            if self.action.target:
                target = "[owner %s]" % self.action.target
            else:
                target = 'owner'
            settarget = "[%s setTarget:%s];" % (varname, target)
        else:
            action = "nil"
            settarget = ""
        if self.shortcut:
            key = self.shortcut.key
            if self.shortcut.flags:
                setkeymask = "[%s setKeyEquivalentModifierMask:%s];" % (varname, self.shortcut.flags)
            else:
                setkeymask = ""
        else:
            key = "nil"
            setkeymask = ""
        return tmpl_replace(**vars())
    

class NSMenu(NSMenuItem):
    def __init__(self, name):
        NSMenuItem.__init__(self, name, None, None)
        self.items = []
    
    def add(self, menu_or_item):
        self.items.append(menu_or_item)
    
    def addItem(self, *args):
        item = NSMenuItem(*args)
        self.add(item)
        return item
    
    def addMenu(self, *args):
        menu = NSMenu(*args)
        self.add(menu)
        return menu
    
    def generate(self, varname, menuname=None):
        if menuname:
            tmpl = """NSMenuItem *_tmpitem = [%%menuname%% addItemWithTitle:@"%%name%%" action:nil keyEquivalent:@""];
            NSMenu *%%varname%% = [[[NSMenu alloc] initWithTitle:@"%%name%%"] autorelease];
            [%%menuname%% setSubmenu:%%varname%% forItem:_tmpitem];
            %%subitemscode%%
            """
        else:
            tmpl = """%%varname%% = [[[NSMenu alloc] initWithTitle:@"%%name%%"] autorelease];
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
        
        
    
