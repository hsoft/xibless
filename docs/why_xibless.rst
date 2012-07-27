============
Why xibless?
============

For many people XCode and its integrated interface builder work fine and to be fair, XCode is a
nice tool. However, it has shortcomings, mostly just annoyances, but still, after a while,
annoyances become... annoying. For example, when a XIB UI reaches a certain level of complexity, you
never know, when doing minor updates, if you mistakenly messed up something else. Because every
modification, however minor it is, changes a big part of the XIB file, you can't tell in the diff
if the modification you've made was exclusively the one you wanted to make. There's also XIB
localization, with its one-xib-copy-per-localization, which is less than optimal but hard to work
around.

Another reason I find interesting is comments. Sometimes, when you design an interface, you do
subtle, but weird and important thing, such as placing a widget here instead of there. Within the
XIB, there's no space to leave a comment on why you did things like that. In code, it's possible
and natural.

In the same vein as comments, code also explain the *nature* of a layout better than the XIB. These
widgets are in a row, this one is placed relatively to this one, this one is placed relatively to
the bottom of the superview, not relatively to the view above it, etc.. To be fair, in this
regard, I think the new layout feature in OS X 10.7 make things better, so this argument might have
less weight now.

It's also easier to spot exceptions. Because using something else than the default margins is
exceptional, the call to the layout method you make with ``margin=42`` stands out. In XCode, it's
not obvious that you purposefully placed that button at a ``6`` margin instead of the default ``8``.

Another interesing perk of code over GUI designers is *logical uniformity*. Let's say that you give
a group of labels a specific font. When you do it, you know why, alright, but when you edit it
later, it's not obvious that this or that group of labels have the exact same font and that it's
meant that way. In a ``xibless`` script, you would do something like::

    myLabels = [label1, label2, label3]
    myFont = Font("My Font Name", 42)
    for label in myLabels:
        label.font = myFont

It is now obvious to the person who edits the UI that these labels are meant to have the same font.

Anyway, I'm not going to try to convince you. If you don't already want to get rid of XCode
and/or XIBs, you probably don't need ``xibless``.
