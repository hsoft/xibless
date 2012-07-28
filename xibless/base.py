import re
from collections import defaultdict, namedtuple

try:
    basestring
except NameError: # python 3
    basestring = str

def upFirstLetter(s):
    return s[0].upper() + s[1:]

def stringArray(strings):
    return "[NSArray arrayWithObjects:%s,nil]" % ','.join(('@"%s"' % s) for s in strings)

def wrapString(s):
    s = s.replace('\n', '\\n').replace('"', '\\"')
    return '@"%s"' % s

globalLocalizationTable = None
globalRunMode = False

def convertValueToObjc(value, requireNSObject=False):
    if value is None:
        return 'nil'
    elif isinstance(value, KeyValueId):
        return value._objcAccessor()
    elif hasattr(value, 'objcValue'):
        return value.objcValue()
    elif isinstance(value, basestring):
        result = wrapString(value)
        if value and globalLocalizationTable:
            result = 'NSLocalizedStringFromTable(%s, @"%s", @"")' % (result, globalLocalizationTable)
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

class CodeTemplate(object):
    def __init__(self, template):
        self._template = template
        self._replacements = {}
    
    def __getattr__(self, key):
        if key in self._replacements:
            return self._replacements[key]
        else:
            raise AttributeError()
    
    def __setattr__(self, key, value):
        if key in ['_template', '_replacements']:
            return object.__setattr__(self, key, value)
        self._replacements[key] = value
    
    def render(self):
        # Because we generate code and that code is likely to contain "{}" braces, it's better if we
        # use more explicit placeholders than the typecal format() method. These placeholders are
        # $name$.
        result = self._template
        replacements = self._replacements
        placeholders = re.findall(r"\$\w+?\$", result)
        while placeholders:
            # We run replacements multiple times because it's possible that one of our replacement
            # strings contain replacement placeholders. We want to perform replacements on those
            # strings too.
            for placeholder in placeholders:
                replacement = str(replacements.get(placeholder[1:-1], ''))
                result = result.replace(placeholder, replacement)
            placeholders = re.findall(r"\$\w+?\$", result)
        return result

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
    
owner = KeyValueId(None, 'owner')
NSApp = KeyValueId(None, 'NSApp')
const = ConstGenerator()
defaults = KeyValueId(None, 'NSUserDefaultsController').sharedUserDefaultsController

Action = namedtuple('Action', 'target selector')

# Use this in properties when you need it to be generated as-is, and not wrapped as a normal string
class Literal(object):
    def __init__(self, value):
        self.value = value
    
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
        elements = set(value.lower().split('+'))
        flags = Flags()
        for ident, flag in SHORTCUT_FLAGS:
            if ident in elements:
                elements.remove(ident)
                flags.add(flag)
        if flags:
            target.properties['keyEquivalentModifierMask'] = flags
        assert len(elements) == 1
        key = list(elements)[0]
        if key in SPECIAL_KEYS:
            key = Literal('stringFromChar({})'.format(SPECIAL_KEYS[key]))
        elif key in REPLACED_KEYS:
            key = NLSTR(REPLACED_KEYS[key])
        else:
            key = NLSTR(key)
        target.properties['keyEquivalent'] = key

Binding = namedtuple('Binding', 'name target keyPath options')

class GeneratedItem(object):
    OBJC_CLASS = 'NSObject'
    # This is a shorthand for setting the self.properties dictionary with the value of the prop in
    # generateInit(). This list contains either Property instances or, to avoid unnecessary
    # verbosity, a string with the property name, which is the equivalent of Property(name).
    PROPERTIES = []
    
    def __init__(self):
        self.creationOrder = globalGenerationCounter.creationToken()
        # In case we are never assigned to a top level variable and thus never given a varname
        self.varname = "_tmp%d" % self.creationOrder
        # properties to be set at generation time. For example, if "editable" is set to False,
        # a "[$varname$ setEditable:NO];" statement will be generated.
        self.properties = {}
        self._bindings = []
    
    #--- Private
    def _generateProperties(self, properties=None):
        result = ''
        if properties is None:
            properties = self.properties
            for prop in self.PROPERTIES:
                if not isinstance(prop, Property):
                    assert isinstance(prop, str)
                    prop = Property(prop)
                prop.setOnTarget(self)
        for key, value in properties.items():
            if value is None:
                continue
            dot_elements = key.split('.')
            accessor = self.accessor
            for dot_element in dot_elements[:-1]:
                accessor = getattr(accessor, dot_element)
            if isinstance(value, GeneratedItem) and not value.generated:
                # Generate an assignment (which is generated by the "value" part of the assignment)
                # so that we set that value after our target item was generated
                setattr(accessor, dot_elements[-1], value)
            else:
                methname = 'set' + upFirstLetter(dot_elements[-1])
                result += accessor._callMethod(methname, value)
        return result
    
    #--- Virtual
    def generateInit(self):
        tmpl = CodeTemplate("$allocinit$\n$setup$\n$setprop$\n")
        tmpl.varname = self.varname
        tmpl.classname = self.OBJC_CLASS
        tmpl.allocinit = "$classname$ *$varname$ = [[[$classname$ alloc] $initmethod$] autorelease];"
        tmpl.initmethod = "init"
        tmpl.setup = ''
        return tmpl
    
    def dependencies(self):
        # Return a list of items on which self depends. We'll make sure that they're generated first.
        return []
    
    #--- Public
    @property
    def accessor(self):
        return KeyValueId(None, self.varname)
    
    @property
    def generated(self):
        return globalGenerationCounter.isGenerated(self)
    
    def bind(self, name, target, keyPath, valueTransformer=None):
        options = {}
        if valueTransformer:
            options[const.NSValueTransformerNameBindingOption] = NLSTR(valueTransformer)
        binding = Binding(NLSTR(name), target, NLSTR(keyPath), options)
        self._bindings.append(binding)
    
    def objcValue(self):
        return self.varname
    
    def generateAssignments(self):
        if self not in KeyValueId.VALUE2KEYS:
            return ""
        assignments = []
        for key in KeyValueId.VALUE2KEYS[self]:
            setmethod = 'set' + upFirstLetter(key._name)
            assignment = key._parent._callMethod(setmethod, self)
            assignments.append(assignment)
        return '\n'.join(assignments)
    
    def generateBindings(self):
        bindings = []
        for binding in self._bindings:
            method = '[{} bind:{} toObject:{} withKeyPath:{} options:{}];'
            if binding.options:
                options = generateDictionary(binding.options)
            else:
                options = 'nil'
            name = convertValueToObjc(binding.name)
            target = convertValueToObjc(binding.target)
            keyPath = convertValueToObjc(binding.keyPath)
            bindings.append(method.format(self.varname, name, target, keyPath, options))
        return '\n'.join(bindings)
    
    def generateFinalize(self):
        # Called after everything has been generated.
        pass
    
    def generate(self, *args, **kwargs):
        result = ''
        for dependency in self.dependencies():
            if isinstance(dependency, GeneratedItem) and not dependency.generated:
                result += dependency.generate()
        inittmpl = self.generateInit(*args, **kwargs)
        inittmpl.setprop = self._generateProperties()
        result += inittmpl.render()
        result += self.generateAssignments()
        if not globalRunMode:
            # We don't generate bindings in "run" mode because bindings can generate crashes if they
            # aren't actually connected to something.
            result += self.generateBindings()
        globalGenerationCounter.addGenerated(self)
        return result
    

class GenerationCounter(object):
    def __init__(self):
        self.reset()
    
    def creationToken(self):
        count = self.creationCount
        self.creationCount += 1
        return count
    
    def addGenerated(self, item):
        self.generatedItems.add(item)
    
    def isGenerated(self, item):
        return item in self.generatedItems
    
    def reset(self):
        self.creationCount = 0
        self.generatedItems = set()
    

globalGenerationCounter = GenerationCounter()