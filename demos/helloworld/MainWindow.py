ownerclass = 'AppDelegate'

# Init
result = Window(330, 110, "Tell me your name!")
result.xProportion = 0.8
result.yProportion = 0.2
result.canResize = False
nameLabel = Label(result, text="Name:")
nameLabel.width = 45
nameField = TextField(result, text="")
helloLabel = Label(result, text="")
button = Button(result, title="Say Hello", action=Action(owner, 'sayHello'))
button.keyEquivalent = "\\r"

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
