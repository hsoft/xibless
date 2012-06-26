# Init
result = Window(200, 200, 250, 200, "All Supported Widgets")
label = Label(result, text="Label")
label.font = Font("Verdana", 12, [FontTrait.Bold, FontTrait.Italic])
textfield = TextField(result, text="TextField")
button = Button(result, title="Button")
checkbox = Checkbox(result, title="Checkbox")

label.packToCorner(Pack.UpperLeft)
label.fill(Pack.Right)
textfield.packRelativeTo(label, side=Pack.Below, align=Pack.Left)
button.packRelativeTo(textfield, side=Pack.Below, align=Pack.Left)
checkbox.packRelativeTo(button, side=Pack.Below, align=Pack.Left)