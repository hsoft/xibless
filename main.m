#import <Cocoa/Cocoa.h>

void populateApplicationMenu(NSMenu *menu)
{
    NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
    NSString * applicationName = [infoDictionary objectForKey:@"CFBundleName"];
    NSMenuItem * item;
    
    item = [menu addItemWithTitle:[NSString stringWithFormat:@"%@ %@", NSLocalizedString(@"About", nil), applicationName]
                           action:@selector(orderFrontStandardAboutPanel:)
                    keyEquivalent:@""];
    [item setTarget:NSApp];
    
    [menu addItem:[NSMenuItem separatorItem]];
    
    item = [menu addItemWithTitle:NSLocalizedString(@"Preferences...", nil)
                           action:NULL
                    keyEquivalent:@","];
    
    [menu addItem:[NSMenuItem separatorItem]];
    
    item = [menu addItemWithTitle:NSLocalizedString(@"Services", nil)
                           action:NULL
                    keyEquivalent:@""];
    NSMenu * servicesMenu = [[[NSMenu alloc] initWithTitle:@"Services"] autorelease];
    [menu setSubmenu:servicesMenu forItem:item];
    [NSApp setServicesMenu:servicesMenu];
    
    [menu addItem:[NSMenuItem separatorItem]];
    
    item = [menu addItemWithTitle:[NSString stringWithFormat:@"%@ %@", NSLocalizedString(@"Hide", nil), applicationName]
                           action:@selector(hide:)
                    keyEquivalent:@"h"];
    [item setTarget:NSApp];
    
    item = [menu addItemWithTitle:NSLocalizedString(@"Hide Others", nil)
                           action:@selector(hideOtherApplications:)
                    keyEquivalent:@"h"];
    [item setKeyEquivalentModifierMask:NSCommandKeyMask | NSAlternateKeyMask];
    [item setTarget:NSApp];
    
    item = [menu addItemWithTitle:NSLocalizedString(@"Show All", nil)
                           action:@selector(unhideAllApplications:)
                    keyEquivalent:@""];
    [item setTarget:NSApp];
    
    [menu addItem:[NSMenuItem separatorItem]];
    
    item = [menu addItemWithTitle:[NSString stringWithFormat:@"%@ %@", NSLocalizedString(@"Quit", nil), applicationName]
                           action:@selector(terminate:)
                    keyEquivalent:@"q"];
    [item setTarget:NSApp];
}

int main(int argc, char *argv[])
{
    [NSApplication sharedApplication];
    NSMenu * mainMenu = [[[NSMenu alloc] initWithTitle:@"MainMenu"] autorelease];
    
    NSMenuItem * item;
    NSMenu * submenu;
    
    // The titles of the menu items are for identification purposes only and shouldn't be localized.
    // The strings in the menu bar come from the submenu titles,
    // except for the application menu, whose title is ignored at runtime.
    item = [mainMenu addItemWithTitle:@"Apple" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:@"Apple"] autorelease];
    [NSApp performSelector:@selector(setAppleMenu:) withObject:submenu];
    populateApplicationMenu(submenu);
    [mainMenu setSubmenu:submenu forItem:item];
    
    item = [mainMenu addItemWithTitle:@"File" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"File", @"The File menu")] autorelease];
    // [self populateFileMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];
    
    item = [mainMenu addItemWithTitle:@"Edit" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"Edit", @"The Edit menu")] autorelease];
    // [self populateEditMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];
    
    /*item = [mainMenu addItemWithTitle:@"View" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"View", @"The View menu")] autorelease];
    [self populateViewMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];*/
    
    item = [mainMenu addItemWithTitle:@"Window" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"Window", @"The Window menu")] autorelease];
    // [self populateWindowMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];
    [NSApp setWindowsMenu:submenu];
    
    item = [mainMenu addItemWithTitle:@"Help" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"Help", @"The Help menu")] autorelease];
    // [self populateHelpMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];
    
    /*item = [mainMenu addItemWithTitle:@"Debug" action:NULL keyEquivalent:@""];
    submenu = [[[NSMenu alloc] initWithTitle:NSLocalizedString(@"Debug", @"The Debug menu")] autorelease];
    [self populateDebugMenu:submenu];
    [mainMenu setSubmenu:submenu forItem:item];*/
    [NSApp setMainMenu:mainMenu];
    [NSApp run];
    return 0;
}