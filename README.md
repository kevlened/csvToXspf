csvToXspf
---------
This converts csv playlists downloaded from sites like [groovebackup](http://groovebackup.com/) to the [xspf](http://xspf.org) playlist format.

Xspf playlists are an open way to store your playlists.

usage: python csvToXspf.py [csv location] [xspf destination]

notes
-----
Python 2.7 must be installed.

This uses Alastair Porter's [python xspf library](https://github.com/alastair/xspf).

Locations in the command line must not contain spaces.

Only artists and song names are currently included in the xspf.

This should work on any csv with the headers [song, artist, album].