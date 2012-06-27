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
around. Anyway, I'm not going to try to convince you. If you don't already want to get rid of XCode
and/or XIBs, you probably don't need ``xibless``.