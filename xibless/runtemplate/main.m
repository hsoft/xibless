#import <Cocoa/Cocoa.h>
#import "MainMenu.h"
#import "MainWindow.h"

int main(int argc, char *argv[])
{
    [NSApplication sharedApplication];
    NSMenu * mainMenu = createMainMenu(nil);
    [NSApp setMainMenu:mainMenu];
    NSWindow *window = createMainWindow(nil);
    [window orderFront:nil];
    [NSApp run];
    return 0;
}