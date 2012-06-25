#import <Cocoa/Cocoa.h>
#import "AppDelegate.h"
#import "MainMenu.h"
#import "MainWindow.h"

int main(int argc, char *argv[])
{
    [NSApplication sharedApplication];
    AppDelegate *appDelegate = [[AppDelegate alloc] init];
    [NSApp setDelegate:appDelegate];
    NSMenu * mainMenu = createMainMenu(nil);
    [NSApp setMainMenu:mainMenu];
    NSWindow *window = createMainWindow(appDelegate);
    [window orderFront:nil];
    [NSApp run];
    return 0;
}