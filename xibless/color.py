from __future__ import division

from .base import GeneratedItem, convertValueToObjc

class Color(GeneratedItem):
    OBJC_CLASS = 'NSColor'
    
    def __init__(self, red, green, blue, alpha=1.0):
        GeneratedItem.__init__(self)
        def adjust(x):
            if isinstance(x, int): # we have a color in the 0-0xff range
                x = x / 0xff
            return x
        
        self.red = adjust(red)
        self.green = adjust(green)
        self.blue = adjust(blue)
        self.alpha = adjust(alpha)
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.allocinit = "$classname$ *$varname$ = [NSColor colorWithDeviceRed:$red$ green:$green$ blue:$blue$ alpha:$alpha$];\n"
        tmpl.red = convertValueToObjc(self.red)
        tmpl.green = convertValueToObjc(self.green)
        tmpl.blue = convertValueToObjc(self.blue)
        tmpl.alpha = convertValueToObjc(self.alpha)
        return tmpl
    
