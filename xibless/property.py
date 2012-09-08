from .types import Literal, KeyValueId, NLSTR, Flags

class Property(object):
    def __init__(self, name, targetName=None):
        if not targetName:
            targetName = name
        self.name = name
        self.targetName = targetName
    
    def __repr__(self):
        return '<{}> {} {}'.format(self.__class__.__name__, self.name, self.targetName)
    
    def _convertValue(self, value):
        return value
    
    def _setProperty(self, target, value):
        target.properties[self.targetName] = self._convertValue(value)
    
    def setOnTarget(self, target):
        if hasattr(target, self.name):
            self._setProperty(target, getattr(target, self.name))
        
    
class ImageProperty(Property):
    def _convertValue(self, value):
        if not value:
            return None
        return Literal(KeyValueId(None, 'NSImage')._callMethod('imageNamed', NLSTR(value), endline=False))
    

class ActionProperty(Property):
    def _setProperty(self, target, value):
        if value is None:
            return
        target.properties['target'] = value.target
        target.properties['action'] = Literal('@selector({})'.format(value.selector))
    
SPECIAL_KEYS = {
    'arrowup': 'NSUpArrowFunctionKey',
    'arrowdown': 'NSDownArrowFunctionKey',
    'arrowleft': 'NSLeftArrowFunctionKey',
    'arrowright': 'NSRightArrowFunctionKey',
}

REPLACED_KEYS = {
    'return': '\\r',
    'enter': '\\x03',
    'esc': '\\e',
    'backspace': '\\b',
}

SHORTCUT_FLAGS = [
    ('cmd', 'NSCommandKeyMask'),
    ('ctrl', 'NSControlKeyMask'),
    ('alt', 'NSAlternateKeyMask'),
    ('shift', 'NSShiftKeyMask'),
]

class KeyShortcutProperty(Property):
    def _setProperty(self, target, value):
        if not value:
            return
        if value.endswith('++'):
            # We have a shortcut with a + sign in it, which messes with our parsing. Make a special
            # case.
            elements = set(value[:-2].lower().split('+')) | {'+', }
        else:
            elements = set(value.lower().split('+'))
        flags = Flags()
        for ident, flag in SHORTCUT_FLAGS:
            if ident in elements:
                elements.remove(ident)
                flags.add(flag)
        if flags:
            target.properties['keyEquivalentModifierMask'] = flags
        else:
            target.properties['keyEquivalentModifierMask'] = 0
        assert len(elements) == 1
        key = list(elements)[0]
        if key in SPECIAL_KEYS:
            key = Literal('stringFromChar({})'.format(SPECIAL_KEYS[key]))
        elif key in REPLACED_KEYS:
            key = NLSTR(REPLACED_KEYS[key])
        else:
            key = NLSTR(key)
        target.properties['keyEquivalent'] = key
