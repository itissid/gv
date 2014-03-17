gv
==

Gerrit Vim plugin.
PS: Bottom of the readme for how much work is done.

Why it exists. A great way to learn VIM scripting and building plugins.

This plugin is meant to do a few simple things as a part of its first draft:

1) Pull the list of your changes(reviews you own) from gerrit code review

2) Select a specific change and look at the latest patch set

3) Display a selected file in the patch set along with a quick fix window.
The quick fix window will show all the abbreviated comments(140 chars) and selecting a comment
will inline it with the file's contents with highlighting.

Later versions may allow one to see diffs and other things.

TODOs
1) Figure out new Oauthing stuff in gerrit. ATM you have to SSH Tunnel to access the REST API.
2) Add a virtualenv from klen/pymode for requests package in the Venv.
3) Organize the code a bit more
