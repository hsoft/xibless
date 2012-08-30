from collections import defaultdict, namedtuple
from . import globalvars

try:
    basestring
except NameError: # python 3
    basestring = str

def stringArray(strings):
    return "[NSArray arrayWithObjects:%s,nil]" % ','.join(('@"%s"' % s) for s in strings)

def wrapString(s):
    s = s.replace('\n', '\\n').replace('"', '\\"')
    return '@"%s"' % s

def convertValueToObjc(value, requireNSObject=False):
    if value is None:
        return 'nil'
    elif isinstance(value, KeyValueId):
        return value._objcAccessor()
    elif hasattr(value, 'objcValue'):
        return value.objcValue()
    elif isinstance(value, basestring):
        result = wrapString(value)
        # '-' is the string we use for menu separators and we don't want to localize these.
        if value and value != '-' and globalvars.globalLocalizationTable:
            result = 'NSLocalizedStringFromTable(%s, @"%s", @"")' % (result, globalvars.globalLocalizationTable)
        return result
    elif isinstance(value, bool):
        result = 'YES' if value else 'NO'
        if requireNSObject:
            result = '[NSNumber numberWithBool:{}]'.format(result)
        return result
    elif isinstance(value, (int, float)):
        result = str(value)
        if requireNSObject:
            if isinstance(value, int):
                method = '[NSNumber numberWithInteger:{}]'
            else:
                method = '[NSNumber numberWithDouble:{}]'
            result = method.format(result)
        return result
    else:
        raise TypeError("Can't figure out the property's type")

def generateDictionary(source):
    elems = []
    for key, value in source.items():
        elems.append(convertValueToObjc(value, requireNSObject=True))
        elems.append(convertValueToObjc(key))
    elems.append('nil')
    return '[NSDictionary dictionaryWithObjectsAndKeys:{}]'.format(','.join(elems))

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
    
    def __repr__(self):
        return '<KeyValueId %s>' % self._objcAccessor()
    
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
    def _objcAccessor(self):
        if self._parent:
            if self._parent._name == 'nil':
                return 'nil'
            else:
                return '[%s %s]' % (self._parent._objcAccessor(), self._name)
        else:
            return self._name
    
    def _callMethod(self, methodname, argument=None, endline=True):
        # For now, this method only supports call to methods of zero or one argument.
        if argument is None:
            result = getattr(self, methodname)._objcAccessor()
        else:
            result = '[%s %s:%s]' % (self._objcAccessor(), methodname, convertValueToObjc(argument))
        if endline:
            result += ';\n'
        return result
    
    def _clear(self):
        for child in self._children.values():
            child._clear()
        self._children.clear()
        for keys in KeyValueId.VALUE2KEYS.values():
            keys.discard(self)
    

class ConstGenerator(object):
    def __getattr__(self, name):
        return Literal(name)
    
Action = namedtuple('Action', 'target selector')

# Use this in properties when you need it to be generated as-is, and not wrapped as a normal string
class Literal(object):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "<Literal %r>" % self.value
    
    def __or__(self, other):
        return Flags([self]) | other
    
    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.value)
    
    def objcValue(self):
        return self.value
    

# Use this for strings that shouldn't be wrapped in NSLocalizedStringFromTable
class NonLocalizableString(object):
    def __init__(self, value):
        self.value = value
    
    def objcValue(self):
        return wrapString(self.value)
    
NLSTR = NonLocalizableString # The full class name can be pretty long sometimes...

# Use this for flags-based properties. Will be converted into a "|" joined literal
class Flags(set):
    def __or__(self, other):
        assert isinstance(other, Literal)
        result = Flags(self)
        result.add(other)
        return result
    
    def objcValue(self):
        elems = ((e.value if isinstance(e, Literal) else e) for e in self)
        return '|'.join(elems)
    
Binding = namedtuple('Binding', 'name target keyPath options')
