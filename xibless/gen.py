import os.path
import tempfile
import shutil
from subprocess import Popen

from . import base
from .base import CodeTemplate, Action, GeneratedItem, owner, NSApp, const
from .view import View, Pack, Size, Rect
from .font import Font, FontFamily, FontSize, FontTrait
from .color import Color
from .menu import Menu, MainMenu
from .window import Window, Panel, PanelStyle
from .button import Button, Checkbox
from .label import Label
from .textfield import TextField, TextAlignment
from .textview import TextView
from .popup import Popup
from .combo import Combobox
from .radio import RadioButtons
from .progress import ProgressIndicator
from .image import ImageView
from .tabview import TabView
from .table import TableView
from .splitview import SplitView

try:
    execfile
except NameError:
    # We're in Python 3
    def execfile(file, globals=globals(), locals=locals()):
        with open(file, "r") as fh:
            exec(fh.read()+"\n", globals, locals)

HEADER_TMPL = """
#import <Cocoa/Cocoa.h>
$ownerimport$

$funcsig$;
"""

UNIT_TMPL = """
$mainimport$
$ownerimport$

$funcsig$
{
$contents$
return result;
}
"""

# ownerless is used by runUI. When running a UI, we take one UI script out of its context, so
# any owner assignment will make code compilation fail. Since we just want to preview the UI, we
# don't need those assignments, so we skip them.
def generate(modulePath, dest, ownerless=False, localizationTable=None):
    dest_basename, dest_ext = os.path.splitext(os.path.basename(dest))
    if dest_ext == '.h':
        dest_header = None
    else:
        if not dest_ext:
            dest += '.m'
        dest_header = os.path.splitext(dest)[0] + '.h'
    base.globalLocalizationTable = localizationTable
    base.globalGenerationCounter.reset()
    to_include = {'owner', 'NSApp', 'const', 'View', 'Size', 'Rect', 'Menu', 'MainMenu', 'Action',
        'Window', 'Panel', 'PanelStyle', 'Button', 'Checkbox', 'Label', 'TextField', 'TextView',
        'Popup', 'Combobox', 'RadioButtons', 'ProgressIndicator', 'ImageView', 'TabView',
        'TableView', 'SplitView', 'Font', 'FontFamily', 'FontSize', 'FontTrait',
        'Color', 'Pack', 'TextAlignment',
    }
    module_globals = {name: globals()[name] for name in to_include}
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
    if ownerimport:
        ownerimport = "#import \"%s\"" % ownerimport
    else:
        ownerimport = ''
    if ownerclass == 'id':
        ownerdecl = "id owner"
    else:
        ownerdecl = "%s *owner" % ownerclass
    if dest_header:
        tmpl.mainimport = "#import \"{}.h\"".format(dest_basename)
    else:
        tmpl.mainimport = "#import <Cocoa/Cocoa.h>"
        tmpl.ownerimport = ownerimport
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
        code = item.generate()
        if code:
            codePieces.append(code)
    for item in toGenerate:
        code = item.generateFinalize()
        if code:
            codePieces.append(code)    
    result = module_locals['result']
    funcsig = "{}* create{}({})".format(result.OBJC_CLASS, dest_basename, ownerdecl)
    tmpl.funcsig = funcsig
    tmpl.contents = '\n'.join(codePieces)
    with open(dest, 'wt') as fp:
        fp.write(tmpl.render())
    if dest_header:
        tmpl = CodeTemplate(HEADER_TMPL)
        tmpl.funcsig = funcsig
        tmpl.ownerimport = ownerimport
        with open(dest_header, 'wt') as fp:
            fp.write(tmpl.render())
        

def runUI(modulePath):
    runtemplatePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runtemplate')
    assert os.path.exists(runtemplatePath)
    tmpPath = tempfile.mkdtemp()
    destPath = os.path.join(tmpPath, 'runtemplate')
    shutil.copytree(runtemplatePath, destPath)
    shutil.copy(modulePath, os.path.join(destPath, 'MainScript.py'))
    cmd = 'cd "%s" && python ./waf configure && python ./waf && open build/RunUI.app -W && cd ../.. && rm -r "%s"' % (destPath, tmpPath)
    p = Popen(cmd, shell=True)
    p.wait()

