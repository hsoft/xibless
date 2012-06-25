import os.path

from .base import CodeTemplate, KeyValueId, Action, GeneratedItem, owner, NSApp, const
from .view import Pack
from .menu import Menu, MainMenu
from .window import Window
from .button import Button
from .label import Label
from .textfield import TextField
from .font import Font, FontFamily, FontSize, FontTrait

try:
    execfile
except NameError:
    # We're in Python 3
    def execfile(file, globals=globals(), locals=locals()):
        with open(file, "r") as fh:
            exec(fh.read()+"\n", globals, locals)

UNIT_TMPL = """
#import <Cocoa/Cocoa.h>

$classname$* create$name$($ownerclass$ *owner)
{
$contents$
return result;
}
"""

def generate(module_path, dest):
    module_globals = {
        'owner': owner,
        'NSApp': NSApp,
        'const': const,
        'Menu': Menu,
        'MainMenu': MainMenu,
        'Action': Action,
        'Window': Window,
        'Button': Button,
        'Label': Label,
        'TextField': TextField,
        'Font': Font,
        'FontFamily': FontFamily,
        'FontSize': FontSize,
        'FontTrait': FontTrait,
        'Pack': Pack,
    }
    module_locals = {}
    execfile(module_path, module_globals, module_locals)
    assert 'result' in module_locals
    tmpl = CodeTemplate(UNIT_TMPL)
    tmpl.name = os.path.splitext(os.path.basename(dest))[0]
    toGenerate = []
    for key, value in module_locals.items():
        if not isinstance(value, GeneratedItem):
            continue
        value.varname = key
        toGenerate.append(value)
    toGenerate.sort(key=lambda x: x.creationOrder)
    codePieces = []
    for item in toGenerate:
        if item.generated:
            continue
        codePieces.append(item.generate())
    result = module_locals['result']
    tmpl.ownerclass = module_locals.get('ownerclass', 'id')
    tmpl.classname = result.OBJC_CLASS
    tmpl.contents = '\n'.join(codePieces)
    fp = open(dest, 'wt')
    fp.write(tmpl.render())
    fp.close()
