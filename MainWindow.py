ownerclass = 'AppDelegate'
result = Window(200, 200, 350, 200, "This is a title")
button = Button(result, title="Hello!", width=100, action=Action(owner, 'fooAction'))
button.font = Font(FontFamily.System, FontSize.RegularControl)
label = Label(result, text="This is a label", width=150)
textfield = TextField(result, text="This is a textfield", width=150)
textfield.packToCorner(Pack.UpperLeft)
button.packRelativeTo(textfield, Pack.Right)
label.packToCorner(Pack.LowerRight)
