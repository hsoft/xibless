import os.path

from .base import tmpl_replace, KeyValueId, Action
from .menu import NSMenu
from .window import NSWindow

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
%%contents%%
return result;
}
"""

def generate(module_path, dest):
    owner = KeyValueId(None, 'owner')
    NSApp = KeyValueId(None, 'NSApp')
    const = KeyValueId(None, 'const', fakeParent=True)
    module_globals = {
        'owner': owner,
        'NSApp': NSApp,
        'const': const,
        'NSMenu': NSMenu,
        'Action': Action,
        'NSWindow': NSWindow,
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
