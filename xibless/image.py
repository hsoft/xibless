from .base import const, KeyValueId, Literal
from .view import View

class ImageView(View):
    OBJC_CLASS = 'NSImageView'
    
    def __init__(self, parent, name, alignment=const.NSImageAlignCenter):
        View.__init__(self, parent, 48, 48)
        self.name = name
        self.alignment = alignment
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        self.properties['image'] = Literal(KeyValueId(None, 'NSImage')._callMethod('imageNamed', self.name, endline=False))
        self.properties['imageAlignment'] = self.alignment
        return tmpl
    
