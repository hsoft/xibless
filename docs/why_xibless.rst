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
widgets are in a row, this one is places relatively to this one, this one is placed relatively to
the bottom of the superview, not relatively to the view above it, etc.. To be faire, in this
regard, I think the new layout feature in OS X 10.7 make things better, so this argument might have
less weight now.

Anyway, I'm not going to try to convince you. If you don't already want to get rid of XCode
and/or XIBs, you probably don't need ``xibless``.
