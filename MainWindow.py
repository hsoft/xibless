ownerclass = 'AppDelegate'
result = NSWindow((200, 200, 250, 150), "This is a title")
button = NSButton(result, (0, 0, 100, 26), "Hello!", Action(owner, 'fooAction'))
button.font = NSFont(FontFamily.System, FontSize.System, [FontTrait.Bold])