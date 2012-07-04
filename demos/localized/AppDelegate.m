#import "AppDelegate.h"

@implementation AppDelegate

@synthesize nameField;
@synthesize helloLabel;

- (void)sayHello
{
    NSString *name = [nameField stringValue];
    NSString *msg = [NSString stringWithFormat:NSLocalizedString(@"Hello %@!", @""), name];
    [helloLabel setStringValue:msg];
}
@end
