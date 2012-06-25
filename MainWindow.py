ownerclass = 'AppDelegate'

# Init
result = Window(200, 200, 330, 130, "Tell me your name!")
nameLabel = Label(result, text="Name:", width=45)
nameField = TextField(result, text="", width=100)
helloLabel = Label(result, text="", width=100)
button = Button(result, title="Say Hello", width=100, action=Action(owner, 'sayHello'))
button.font = Font(FontFamily.System, FontSize.RegularControl)

# Owner Assignments
owner.nameField = nameField
owner.helloLabel = helloLabel

# Layout
nameLabel.packToCorner(Pack.UpperLeft)
nameField.packRelativeTo(nameLabel, Pack.Right)
nameField.fill(Pack.Right)
helloLabel.packRelativeTo(nameLabel, Pack.Below)
helloLabel.fill(Pack.Right)
button.packRelativeTo(helloLabel, Pack.Below)
nameField.setAnchor(Pack.UpperLeft, growX=True)
helloLabel.setAnchor(Pack.UpperLeft, growX=True)
