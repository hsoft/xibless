ownerclass = 'AppDelegate'
result = NSMenu("foo")
result.addItem("bar", Action('', 'fooAction'), 'cmd+shift+alt+f')
bar = result.addMenu("barfoo")
bar.addItem("baz")
bar.addItem("bleh")