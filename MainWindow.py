ownerclass = 'AppDelegate'
result = Window((200, 200, 250, 150), "This is a title")
button = Button(result, (0, 0, 100, 26), "Hello!", Action(owner, 'fooAction'))
button.font = Font(FontFamily.System, FontSize.RegularControl)
label = Label(result, (0, 35, 150, 26), "This is a label")
textfield = TextField(result, (0, 60, 150, 22), "This is a textfield")
