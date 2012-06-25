result = MainMenu("MyApp")

# Although the main menu contains a bunch of menu items, it can be tweaked afterwards.
result.editMenu.addItem("foo", index=3)
result.windowMenu.removeItem(index=1)