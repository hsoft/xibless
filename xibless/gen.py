import os.path
import tempfile
import shutil
from subprocess import Popen

from .base import CodeTemplate, KeyValueId, Action, GeneratedItem, owner, NSApp, const
from .view import Pack
from .menu import Menu, MainMenu
from .window import Window
from .button import Button, Checkbox
from .label import Label
from .textfield import TextField
from .popup import Popup
from .combo import Combobox
from .radio import RadioButtons
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
$ownerimport$

$classname$* create$name$($ownerdecl$)
{
$contents$
return result;
}
"""

# ownerless is used by runUI. When running a UI, we take one UI script out of its context, so
# any owner assignment will make code compilation fail. Since we just want to preview the UI, we
# don't need those assignments, so we skip them.
def generate(modulePath, dest, ownerless=False):
    module_globals = {
        'owner': owner,
        'NSApp': NSApp,
        'const': const,
        'Menu': Menu,
        'MainMenu': MainMenu,
        'Action': Action,
        'Window': Window,
        'Button': Button,
        'Checkbox': Checkbox,
        'Label': Label,
        'TextField': TextField,
        'Popup': Popup,
        'Combobox': Combobox,
        'RadioButtons': RadioButtons,
        'Font': Font,
        'FontFamily': FontFamily,
        'FontSize': FontSize,
        'FontTrait': FontTrait,
        'Pack': Pack,
    }
    module_locals = {}
    execfile(modulePath, module_globals, module_locals)
    assert 'result' in module_locals
    tmpl = CodeTemplate(UNIT_TMPL)
    if ownerless:
        owner._clear()
        owner._name = 'nil'
        ownerclass = 'id'
        ownerimport = None
    else:
        ownerclass = module_locals.get('ownerclass', 'id')
        ownerimport = module_locals.get('ownerimport')
    if ownerclass == 'id':
        tmpl.ownerdecl = "id owner"
    else:
        tmpl.ownerdecl = "%s *owner" % ownerclass
    if ownerimport:
        tmpl.ownerimport = "#import \"%s\"" % ownerimport
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
    tmpl.classname = result.OBJC_CLASS
    tmpl.contents = '\n'.join(codePieces)
    fp = open(dest, 'wt')
    fp.write(tmpl.render())
    fp.close()

def runUI(modulePath):
    runtemplatePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runtemplate')
    assert os.path.exists(runtemplatePath)
    tmpPath = tempfile.mkdtemp()
    destPath = os.path.join(tmpPath, 'runtemplate')
    shutil.copytree(runtemplatePath, destPath)
    shutil.copy(modulePath, os.path.join(destPath, 'MainWindow.py'))
    cmd = 'cd "%s" && python ./waf configure && python ./waf && open build/RunUI.app -W && cd ../.. && rm -r "%s"' % (destPath, tmpPath)
    p = Popen(cmd, shell=True)
    p.wait()

