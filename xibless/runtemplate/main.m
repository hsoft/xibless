#import <Cocoa/Cocoa.h>
#import "MainMenu.h"
#import "MainScript.h"

int main(int argc, char *argv[])
{
    [NSApplication sharedApplication];
    NSMenu * mainMenu = createMainMenu(nil);
    [NSApp setMainMenu:mainMenu];
    id result = createMainScript(nil);
    NSWindow *window;
    if ([result isKindOfClass:[NSWindow class]]) {
        window = (NSWindow *)result;
    }
    else if ([result isKindOfClass:[NSView class]]) {
        NSView *view = (NSView *)result;
        NSRect r = [view frame];
        r.origin.x = 500;
        r.origin.y = 500;
        window = [[NSWindow alloc] initWithContentRect:r
            styleMask:NSTitledWindowMask|NSClosableWindowMask|NSResizableWindowMask|NSMiniaturizableWindowMask
            backing:NSBackingStoreBuffered defer:NO];
        [[window contentView] addSubview:view];
        [view setAutoresizingMask:NSViewWidthSizable|NSViewHeightSizable|NSViewMaxXMargin|NSViewMinYMargin];
    }
    else {
        NSLog(@"UI Script results has to be either a window or a view.");
        return 1;
    }
    [window orderFront:nil];
    [NSApp run];
    return 0;
}