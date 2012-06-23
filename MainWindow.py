ownerclass = 'AppDelegate'
result = NSWindow((200, 200, 250, 150), "This is a title")
font = NSFont(FontFamily.System, FontSize.System, [FontTrait.Bold])
button = NSButton(result, (0, 0, 100, 26), "Hello!", Action(owner, 'fooAction'))
button.font = font