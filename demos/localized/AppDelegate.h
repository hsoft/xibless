#import <Cocoa/Cocoa.h>

@interface AppDelegate : NSObject
{
    NSTextField *nameField;
    NSTextField *helloLabel;
}

@property (readwrite, assign) NSTextField *nameField;
@property (readwrite, assign) NSTextField *helloLabel;

- (void)sayHello;
@end