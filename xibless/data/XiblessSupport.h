#import <Cocoa/Cocoa.h>

@interface XiblessToolbarDelegate : NSObject <NSToolbarDelegate>
{
    NSMutableDictionary *items;
    NSArray *defaultItems;
}

- (void)addItem:(NSToolbarItem *)aItem;
- (void)setDefaultItems:(NSArray *)aDefaultItems;
@end

NSString* stringFromChar(unichar c);
