import os.path as op
import tempfile
import shutil
from subprocess import Popen

from . import base
from .base import CodeTemplate, GeneratedItem, owner, NSApp, const, defaults
from .types import Action
from .control import ControlSize
from .view import View, Pack, Size, Rect
from .font import Font, FontFamily, FontSize, FontTrait
from .color import Color
from .formatter import NumberFormatter, NumberStyle
from .menu import Menu, MainMenu
from .window import Window, Panel, PanelStyle
from .button import Button, Checkbox
from .textfield import TextField, Label, SearchField, TextAlignment
from .textview import TextView
from .popup import Popup
from .combo import Combobox
from .radio import RadioButtons
from .progress import ProgressIndicator
from .image import ImageView
from .tabview import TabView
from .table import TableView, ListView, OutlineView
from .splitview import SplitView
from .segment import SegmentedControl
from .slider import Slider
from .layout import HLayout, VLayout

try:
    execfile
except NameError:
    # We're in Python 3
    def execfile(file, globals=globals(), locals=locals()):
        with open(file, "r") as fh:
            exec(fh.read()+"\n", globals, locals)

HEADER_TMPL = """
#import "XiblessSupport.h"
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

# When running a UI (in `runmode`), we take one UI script out of its context, so
# any owner assignment will make code compilation fail. Since we just want to preview the UI, we
# don't need those assignments, so we skip them. Moreover, we revert all instance which had their
# OBJC_CLASS attribute set because this is also going to make complication fail.
def generate(modulePath, dest, runmode=False, localizationTable=None, args=None):
    if args is None:
        args = {}
    dest_basename, dest_ext = op.splitext(op.basename(dest))
    if dest_ext == '.h':
        dest_header = None
    else:
        if not dest_ext:
            dest += '.m'
        dest_header = op.splitext(dest)[0] + '.h'
    base.globalLocalizationTable = localizationTable
    base.globalRunMode = runmode
    base.globalGenerationCounter.reset()
    to_include = {'owner', 'NSApp', 'const', 'defaults', 'View', 'Size', 'Rect', 'ControlSize',
        'Menu', 'MainMenu', 'Action', 'Window', 'Panel', 'PanelStyle', 'Button', 'Checkbox',
        'Label', 'TextField', 'TextView', 'SearchField', 'Popup', 'Combobox', 'RadioButtons',
        'ProgressIndicator', 'ImageView', 'TabView', 'TableView', 'ListView', 'OutlineView',
        'SplitView', 'Font', 'FontFamily', 'FontSize', 'FontTrait', 'Color', 'Pack',
        'TextAlignment', 'HLayout', 'VLayout', 'SegmentedControl', 'Slider', 'NumberFormatter',
        'NumberStyle',
    }
    module_globals = {name: globals()[name] for name in to_include}
    module_globals['args'] = args
    module_locals = {}
    execfile(modulePath, module_globals, module_locals)
    assert 'result' in module_locals
    tmpl = CodeTemplate(UNIT_TMPL)
    if runmode:
        owner._clear()
        owner._name = 'nil'
        ownerclass = 'id'
        ownerimport = None
        for value in module_locals.values():
            if hasattr(value, 'OBJC_CLASS'):
                value.OBJC_CLASS = value.__class__.OBJC_CLASS
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
        tmpl.mainimport = "#import \"XiblessSupport.h\""
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
        fp.write(tidyCode(tmpl.render()))
    if dest_header:
        tmpl = CodeTemplate(HEADER_TMPL)
        tmpl.funcsig = funcsig
        tmpl.ownerimport = ownerimport
        with open(dest_header, 'wt') as fp:
            fp.write(tidyCode(tmpl.render()))
    copy_support_unit(op.dirname(dest))

def runUI(modulePath):
    runtemplatePath = op.join(op.dirname(op.abspath(__file__)), 'runtemplate')
    assert op.exists(runtemplatePath)
    tmpPath = tempfile.mkdtemp()
    destPath = op.join(tmpPath, 'runtemplate')
    shutil.copytree(runtemplatePath, destPath)
    shutil.copy(modulePath, op.join(destPath, 'MainScript.py'))
    cmd = 'cd "%s" && python ./waf configure && python ./waf && open build/RunUI.app -W && cd ../.. && rm -r "%s"' % (destPath, tmpPath)
    p = Popen(cmd, shell=True)
    p.wait()

def tidyCode(code):
    lines = (l.strip() for l in code.split('\n'))
    result = []
    level = 0
    for line in lines:
        if not line:
            if result and result[-1] != '':
                result.append('')
            continue
        level -= line.count('}')
        result.append((' ' * (level * 4)) + line)
        level += line.count('{')
    return '\n'.join(result)

def copy_support_unit(destfolder):
    DATA_PATH = op.join(op.dirname(__file__), 'data')
    if not op.exists(destfolder):
        os.makedirs(destfolder)
    shutil.copy(op.join(DATA_PATH, 'XiblessSupport.h'), destfolder)
    shutil.copy(op.join(DATA_PATH, 'XiblessSupport.m'), destfolder)
