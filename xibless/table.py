from .base import GeneratedItem, convertValueToObjc, KeyValueId
from .view import View

class TableColumn(GeneratedItem):
    OBJC_CLASS = 'NSTableColumn'
    
    def __init__(self, table, identifier, title, width):
        GeneratedItem.__init__(self)
        self.table = table
        self.identifier = identifier
        self.title = title
        self.width = width
        self.font = table.font
        self.editable = True
    
    def dependencies(self):
        return [self.font]
    
    def generateInit(self):
        tmpl = GeneratedItem.generateInit(self)
        tmpl.initmethod = "initWithIdentifier:$identifier$"
        tmpl.identifier = convertValueToObjc(self.identifier)
        self.properties['headerCell.stringValue'] = self.title
        if self.font:
            self.properties['dataCell.font'] = self.font
        self.properties['width'] = self.width
        self.properties['editable'] = self.editable
        return tmpl
    

class TableView(View):
    OBJC_CLASS = 'NSTableView'
    
    def __init__(self, parent):
        View.__init__(self, parent, 100, 100)
        self.columns = []
        self.font = None
        self.allowsColumnReordering = None
        self.allowsColumnResizing = None
        self.allowsColumnSelection = None
        self.allowsEmptySelection = None
        self.allowsMultipleSelection = None
        self.allowsTypeSelect = None
    
    def addColumn(self, identifier, title, width):
        column = TableColumn(self, identifier, title, width)
        self.columns.append(column)
        return column
    
    def generateInit(self):
        tmpl = View.generateInit(self)
        viewsetup = """NSScrollView *$varname$_container = [[[NSScrollView alloc] initWithFrame:$rect$] autorelease];
            [$varname$_container setDocumentView:$varname$];
            [$varname$_container setHasVerticalScroller:YES];
            [$varname$_container setHasHorizontalScroller:YES];
            [$varname$_container setAutohidesScrollers:YES];
            [$varname$_container setBorderType:NSBezelBorder];
            [$varname$_container setAutoresizingMask:$autoresize$];
        """
        tmpl.autoresize = convertValueToObjc(self.properties['autoresizingMask'])
        for column in self.columns:
            colcode = column.generate()
            colcode += "[$varname$ addTableColumn:%s];\n" % column.varname
            viewsetup += colcode
        tmpl.viewsetup = viewsetup
        self.properties['allowsColumnReordering'] = self.allowsColumnReordering
        self.properties['allowsColumnResizing'] = self.allowsColumnResizing
        self.properties['allowsColumnSelection'] = self.allowsColumnSelection
        self.properties['allowsEmptySelection'] = self.allowsEmptySelection
        self.properties['allowsMultipleSelection'] = self.allowsMultipleSelection
        self.properties['allowsTypeSelect'] = self.allowsTypeSelect
        return tmpl
    
    def generateAddToParent(self):
        container = KeyValueId(None, self.varname + '_container')
        return self.parent.generateAddSubview(container)
    

    