from __future__ import division, print_function

from .base import stringArray
from .view import View

class RadioButtons(View):
    OBJC_CLASS = 'NSMatrix'
    
    def __init__(self, parent, items, columns=1):
        View.__init__(self, parent, 80, 40)
        self.items = items
        self.columns = columns
    
    def generateInit(self):
        tmpl = View.generateInit(self)
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
        rows = len(self.items) // self.columns
        if len(self.items) % self.columns:
            print("WARNING: A radio button has a number of items that is uneven with it's columns.")
            rows += 1
        tmpl.rows = rows
        tmpl.radiostrings = stringArray(self.items)
        return tmpl
