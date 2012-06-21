#import <Cocoa/Cocoa.h>
#import "AppDelegate.h"
#import "MainMenu.h"

int main(int argc, char *argv[])
{
    [NSApplication sharedApplication];
    AppDelegate *appDelegate = [[AppDelegate alloc] init];
    [NSApp setDelegate:appDelegate];
    NSMenu * mainMenu = createMainMenu(appDelegate);
    [NSApp setMainMenu:mainMenu];
    [NSApp run];
    return 0;
}