from .base import const
from .property import ImageProperty
from .view import View

class ImageView(View):
    OBJC_CLASS = 'NSImageView'
    PROPERTIES = View.PROPERTIES + [ImageProperty('name', 'image'), 'imageAlignment']
    
    def __init__(self, parent, name, alignment=const.NSImageAlignCenter):
        View.__init__(self, parent, 48, 48)
        self.name = name
        self.alignment = alignment
    
