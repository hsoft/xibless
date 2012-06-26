from .base import GeneratedItem

class FontFamily(object):
    System = object()
    Label = object()
    Menu = object()
    Menubar = object()
    Message = object()
    Palette = object()
    Titlebar = object()
    Tooltips = object()
    
class FontSize(object):
    System = object()
    SmallSystem = object()
    Label = object()
    RegularControl = object()
    SmallControl = object()
    MiniControl = object()
    
    MethodConsts = {System, SmallSystem, Label}
    ControlConsts = {RegularControl, SmallControl, MiniControl}

class FontTrait(object):
    Bold = object()
    Italic = object()
    # Strikethrough = object() # not supported yet

FAMILY2METHOD = {
    FontFamily.System: 'systemFontOfSize',
    FontFamily.Label: 'labelFontOfSize',
    FontFamily.Menu: 'menuFontOfSize',
    FontFamily.Menubar: 'menuBarFontOfSize',
    FontFamily.Message: 'messageFontOfSize',
    FontFamily.Palette: 'paletteFontOfSize',
    FontFamily.Titlebar: 'titleBarFontOfSize',
    FontFamily.Tooltips: 'toolTipsFontOfSize',
}

SIZE2METHOD = {
    FontSize.System: 'systemFontSize',
    FontSize.SmallSystem: 'smallSystemFontSize',
    FontSize.Label: 'labelFontSize',
}

SIZE2CONTROLCONST = {
    FontSize.RegularControl: 'NSRegularControlSize',
    FontSize.SmallControl: 'NSSmallControlSize',
    FontSize.MiniControl: 'NSMiniControlSize',
}

TRAIT2CONST = {
    FontTrait.Bold: 'NSBoldFontMask',
    FontTrait.Italic: 'NSItalicFontMask',
}

class Font(GeneratedItem):
    OBJC_CLASS = 'NSFont'
    
    def __init__(self, family, size, traits=None):
        # family and size can be a "real" value (str and float) or one of the constants.
        GeneratedItem.__init__(self)
        self.family = family
        self.size = size
        if traits:
            self.traits = set(traits)
        else:
            self.traits = set()
    
    def generateInit(self):
        # We use code blocks to avoid tmp variable name clashes.
        tmpl = GeneratedItem.generateInit(self)
        tmpl.allocinit = """NSFont *$varname$;
            {
                CGFloat _fontSize = $sizeinit$;
                $varname$ = [NSFont $fontinit$];
            }
        """
        if self.family in FAMILY2METHOD:
            tmpl.fontinit = "%s:_fontSize" % FAMILY2METHOD[self.family]
        else:
            tmpl.fontinit = "fontWithName:@\"%s\" size:_fontSize" % self.family
        if self.size in SIZE2METHOD:
            tmpl.sizeinit = "[NSFont %s]" % SIZE2METHOD[self.size]
        elif self.size in SIZE2CONTROLCONST:
            tmpl.sizeinit = "[NSFont systemFontSizeForControlSize:%s]" % SIZE2CONTROLCONST[self.size]
        else:
            tmpl.sizeinit = str(self.size)
        if self.traits:
            traits = '|'.join(TRAIT2CONST[trait] for trait in self.traits)
            tmpl.setup = "$varname$ = [[NSFontManager sharedFontManager] convertFont:$varname$ toHaveTrait:%s];\n" % traits
        return tmpl
    
