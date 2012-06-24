from collections import defaultdict

class CodeTemplate(object):
    def __init__(self, template):
        self._template = template
        self._replacements = {}
    
    def __setattr__(self, key, value):
        if key in ['_template', '_replacements']:
            return object.__setattr__(self, key, value)
        self._replacements[key] = value
    
    def render(self):
        # Because we generate code and that code is likely to contain "{}" braces, it's better if we
        # use more explicit placeholders than the typecal format() method. These placeholders are
        # %%name%%.
        result = self._template
        replacements = self._replacements
        for placeholder, replacement in replacements.items():
            wrapped_placeholder = '%%{}%%'.format(placeholder)
            if wrapped_placeholder not in result:
                continue
            result = result.replace(wrapped_placeholder, replacement)
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
    def _dottedAccessor(self):
        if self._parent and not self._parent._fakeParent:
            return '%s.%s' % (self._parent._dottedAccessor(), self._name)
        else:
            return self._name
    
    def _objcAccessor(self):
        if self._parent and not self._parent._fakeParent:
            return '[%s %s]' % (self._parent._objcAccessor(), self._name)
        else:
            return self._name

class Action(object):
    def __init__(self, target, selector):
        self.target = target
        self.selector = selector
    
    def generate(self, sender):
        tmpl = CodeTemplate("""[%%sender%% setTarget:%%target%%];
        [%%sender%% setAction:%%selector%%];
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
        

class GeneratedItem(object):
    CREATION_ORDER_COUNTER = 0
    def __init__(self):
        self.creationOrder = GeneratedItem.CREATION_ORDER_COUNTER
        GeneratedItem.CREATION_ORDER_COUNTER += 1
        self.generated = False
        # In case we are never assigned to a top level variable and thus never given a varname
        self.varname = "_tmp%d" % self.creationOrder
    
    #--- Virtual
    def generateInit(self):
        # Return a string containing the code to create an initialize the item.
        raise NotImplementedError()
    
    def dependencies(self):
        # Return a list of items on which self depends. We'll make sure that they're generated first.
        return []
    
    #--- Public
    def template(self, tmpl):
        result = CodeTemplate(tmpl)
        result.varname = self.varname
        return result
    
    def generateAssignments(self):
        if self not in KeyValueId.VALUE2KEYS:
            return ""
        assignments = []
        for key in KeyValueId.VALUE2KEYS[self]:
            parentAccessor = key._parent._objcAccessor()
            setmethod = 'set' + key._name[0].upper() + key._name[1:]
            assignment = "[%s %s: %s];" % (parentAccessor, setmethod, self.varname)
            assignments.append(assignment)
        return '\n'.join(assignments)
    
    def generate(self, *args, **kwargs):
        result = ''
        for dependency in self.dependencies():
            result += dependency.generate()
        result += self.generateInit(*args, **kwargs)
        result += self.generateAssignments()
        self.generated = True
        return result
    
