import re
from collections import defaultdict

try:
    basestring
except NameError: # python 3
    basestring = str

def upFirstLetter(s):
    return s[0].upper() + s[1:]

def stringArray(strings):
    return "[NSArray arrayWithObjects:%s,nil]" % ','.join(('@"%s"' % s) for s in strings)

globalLocalizationTable = None

def convertValueToObjc(value):
    if value is None:
        return 'nil'
    elif isinstance(value, GeneratedItem):
        return value.varname
    elif isinstance(value, KeyValueId):
        return value._objcAccessor()
    elif isinstance(value, Literal):
        return value.value
    elif isinstance(value, basestring):
        value = value.replace('\n', '\\n')
        result = '@"%s"' % value
        if value and globalLocalizationTable:
            result = 'NSLocalizedStringFromTable(%s, @"%s", @"")' % (result, globalLocalizationTable)
        return result
    elif isinstance(value, bool):
        return 'YES' if value else 'NO'
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        raise TypeError("Can't figure out the property's type")

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
    def __init__(self, parent, name, fakeParent=False):
        self._parent = parent
        self._name = name
        # set fakeParent to True when you want to ignore this KeyValueId in accessors. You can use
        # this for stuff like "const.NSOnState" where we want the accessor to be "NSOnState", not
        # [const NSOnState];
        self._fakeParent = fakeParent
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
        if self._parent and not self._parent._fakeParent:
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
    

owner = KeyValueId(None, 'owner')
NSApp = KeyValueId(None, 'NSApp')
const = KeyValueId(None, 'const', fakeParent=True)

class Action(object):
    def __init__(self, target, selector):
        self.target = target
        self.selector = selector
    
    def generate(self, sender):
        tmpl = CodeTemplate("""[$sender$ setTarget:$target$];
        [$sender$ setAction:$selector$];
        """)
        tmpl.sender = sender
        tmpl.selector = "@selector(%s)" % self.selector
        if self.target:
            tmpl.target = self.target._objcAccessor()
        else:
            tmpl.target = 'nil'
        return tmpl.render()
    

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
        

# Use this in properties when you need it to be generated as-is, and not wrapped as a normal string
class Literal(object):
    def __init__(self, value):
        self.value = value
    

class GeneratedItem(object):
    OBJC_CLASS = 'NSObject'
    
    def __init__(self):
        self.creationOrder = globalGenerationCounter.creationToken()
        # In case we are never assigned to a top level variable and thus never given a varname
        self.varname = "_tmp%d" % self.creationOrder
        # properties to be set at generation time. For example, if "editable" is set to False,
        # a "[$varname$ setEditable:NO];" statement will be generated.
        self.properties = {}
    
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
    
    def generateAssignments(self):
        if self not in KeyValueId.VALUE2KEYS:
            return ""
        assignments = []
        for key in KeyValueId.VALUE2KEYS[self]:
            setmethod = 'set' + upFirstLetter(key._name)
            assignment = key._parent._callMethod(setmethod, self)
            assignments.append(assignment)
        return '\n'.join(assignments)
    
    def generateFinalize(self):
        # Called after everything has been generated.
        pass
    
    def generate(self, *args, **kwargs):
        result = ''
        for dependency in self.dependencies():
            if isinstance(dependency, GeneratedItem) and not dependency.generated:
                result += dependency.generate()
        inittmpl = self.generateInit(*args, **kwargs)
        setprop = ''
        for key, value in self.properties.items():
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
                setprop += accessor._callMethod(methname, value)
        inittmpl.setprop = setprop
        result += inittmpl.render()
        result += self.generateAssignments()
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