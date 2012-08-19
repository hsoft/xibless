from __future__ import division, print_function

from .types import stringArray
from .control import Control, ControlHeights

class RadioButtons(Control):
    OBJC_CLASS = 'NSMatrix'
    
    def __init__(self, parent, items, columns=1):
        self.items = items
        self.columns = columns
        Control.__init__(self, parent, 80, 40)
    
    def _getRowCount(self):
        rows = len(self.items) // self.columns
        if len(self.items) % self.columns:
            print("WARNING: A radio button has a number of items that is uneven with it's columns.")
            rows += 1
        return rows
    
    def _getControlHeights(self):
        # Our control height depends on our number of rows
        result = Control._getControlHeights(self)
        rows = self._getRowCount()
        heights = (x*rows for x in result)
        return ControlHeights(*heights)
    
    def generateInit(self):
        tmpl = Control.generateInit(self)
        tmpl.allocinit = """
        NSMatrix *$varname$;
        {
            NSButtonCell *_radioPrototype = [[[NSButtonCell alloc] init] autorelease];
            [_radioPrototype setButtonType:NSRadioButton];
            NSInteger _rows = $rows$;
            NSInteger _cols = $cols$;
            $varname$ = [[NSMatrix alloc] initWithFrame:$rect$ mode:NSRadioModeMatrix prototype:_radioPrototype numberOfRows:_rows numberOfColumns:_cols];
            NSArray *_radioStrings = $radiostrings$;
            NSInteger _i;
            for (_i=0; _i<[_radioStrings count]; _i++) {
                NSInteger _row = _i / _cols;
                NSInteger _col = _i % _cols;
                NSCell *_radioButton = [$varname$ cellAtRow:_row column:_col];
                [_radioButton setTitle:[_radioStrings objectAtIndex:_i]];
            }
        }
        """
        tmpl.cols = self.columns
        tmpl.rows = self._getRowCount()
        tmpl.radiostrings = stringArray(self.items)
        self.properties['autosizesCells'] = True
        return tmpl
