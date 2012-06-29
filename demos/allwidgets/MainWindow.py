# Init
result = Window(200, 200, 250, 300, "All Supported Widgets")
tabView = TabView(result)
fooTab = tabView.addTab("foo")
barTab = tabView.addTab("bar")
bazTab = tabView.addTab("baz")
label = Label(fooTab.view, text="Label")
label.font = Font("Verdana", 12, [FontTrait.Bold, FontTrait.Italic])
textfield = TextField(fooTab.view, text="TextField")
button = Button(fooTab.view, title="Button")
checkbox = Checkbox(fooTab.view, title="Checkbox")
popup = Popup(barTab.view, items=["One", "Two", "Three"])
combobox = Combobox(barTab.view, items=["One", "Two", "Three"])
combobox.autoComplete = True
radioButtons = RadioButtons(barTab.view, items=["One", "Two", "Three", "Four"], columns=2)
radioButtons.width = 150
radioButtons.height = 50
table = TableView(bazTab.view)
table.addColumn("col1", title="Column 1", width=50)
table.addColumn("col2", title="Column 2", width=100)
table.addColumn("col3", title="Column 3", width=150)

tabView.packToCorner(Pack.UpperLeft)
tabView.fill(Pack.Right)
tabView.fill(Pack.Below)
tabView.setAnchor(Pack.UpperLeft, growX=True, growY=True)

# foo tab
label.packToCorner(Pack.UpperLeft)
label.fill(Pack.Right)
textfield.packRelativeTo(label, side=Pack.Below, align=Pack.Left)
button.packRelativeTo(textfield, side=Pack.Below, align=Pack.Left)
checkbox.packRelativeTo(button, side=Pack.Below, align=Pack.Left)

#bar tab
popup.packToCorner(Pack.UpperLeft)
combobox.packRelativeTo(popup, side=Pack.Below, align=Pack.Left)
radioButtons.packRelativeTo(combobox, side=Pack.Below, align=Pack.Left)

#baz tab
table.packToCorner(Pack.UpperLeft)
table.fill(Pack.Right)
table.fill(Pack.Below)
table.setAnchor(Pack.UpperLeft, growX=True, growY=True)