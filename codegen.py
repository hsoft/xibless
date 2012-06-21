import os.path
import importlib
from collections import namedtuple, defaultdict

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
    owner = KeyValueId(None, 'owner')
    NSApp = KeyValueId(None, 'NSApp')
    module_globals = {
        'owner': owner,
        'NSApp': NSApp,
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


class KeyValueId(object):
    # When we set an KeyValueId attribute in our source file, there no convenient way of saying,
    # at the codegen phase "this is exactly when this value was set, so I'll insert code to assign
    # this value here." What we can do, however, is having a dictionary of all keys a certain value
    # was assigned to and when we create the code for that value, we insert assignments right after.
    VALUE2KEYS = defaultdict(set)
    def __init__(self, parent, name):
        self._parent = parent
        self._name = name
        self._children = {}
    
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        if name in self._children:
            result = self._children[name]
        else:
            result = KeyValueId(self, name)
            self._children[name] = result
        return result
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        key = getattr(self, name)
        KeyValueId.VALUE2KEYS[value].add(key)
    
    # the methods below aren't actually private, it's just that we prepend them with underscores to
    # avoid name clashes.
    def _dotted_accessor(self):
        if self._parent:
            return '%s.%s' % (self._parent._dotted_accessor(), self._name)
        else:
            return self._name
    
    def _objc_accessor(self):
        if self._parent:
            return '[%s %s]' % (self._parent._objc_accessor(), self._name)
        else:
            return self._name

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
        

class GeneratedItem(object):
    def generateAssignments(self, varname):
        if self not in KeyValueId.VALUE2KEYS:
            return ""
        assignments = []
        for key in KeyValueId.VALUE2KEYS[self]:
            parentAccessor = key._parent._objc_accessor()
            setmethod = 'set' + key._name[0].upper() + key._name[1:]
            assignment = "[%s %s: %s];" % (parentAccessor, setmethod, varname)
            assignments.append(assignment)
        return '\n'.join(assignments)
    
    def generate(self, varname, *args, **kwargs):
        result = self.generateInit(varname, *args, **kwargs)
        result += self.generateAssignments(varname)
        return result

class NSMenuItem(GeneratedItem):
    def __init__(self, name, action=None, shortcut=None):
        GeneratedItem.__init__(self)
        self.name = name
        self.action = action
        if shortcut and not isinstance(shortcut, KeyShortcut):
            shortcut = KeyShortcut(shortcut)
        self.shortcut = shortcut
    
    def generateInit(self, varname, menuname):
        if self.name == "-":
            tmpl = "[%%menuname%% addItem:[NSMenuItem separatorItem]];\n"
        else:
            tmpl = """NSMenuItem *%%varname%% = [%%menuname%% addItemWithTitle:@"%%name%%" action:%%action%% keyEquivalent:@"%%key%%"];
            %%settarget%%
            %%setkeymask%%
            """
        name = self.name
        if self.action:
            action = "@selector(%s)" % self.action.selector
            if self.action.target:
                target = self.action.target._objc_accessor()
            else:
                target = 'nil'
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
    
    def addSeparator(self):
        return self.addItem("-")
    
    def addMenu(self, *args):
        menu = NSMenu(*args)
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
        
        
    
