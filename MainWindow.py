ownerclass = 'AppDelegate'

# Init
result = Window(200, 200, 330, 130, "Tell me your name!")
nameLabel = Label(result, text="Name:")
nameLabel.width = 45
nameField = TextField(result, text="")
helloLabel = Label(result, text="")
button = Button(result, title="Say Hello", action=Action(owner, 'sayHello'))

# Owner Assignments
owner.nameField = nameField
owner.helloLabel = helloLabel

# Layout
nameLabel.packToCorner(Pack.UpperLeft)
nameField.packRelativeTo(nameLabel, Pack.Right, Pack.Middle)
nameField.fill(Pack.Right)
helloLabel.packRelativeTo(nameLabel, Pack.Below, Pack.Left)
helloLabel.fill(Pack.Right)
button.packRelativeTo(helloLabel, Pack.Below, Pack.Right)
nameField.setAnchor(Pack.UpperLeft, growX=True)
helloLabel.setAnchor(Pack.UpperLeft, growX=True)
button.setAnchor(Pack.UpperRight)
