# AccountScrubber-for-Reddit
This goes through and tries to systematically clean out your account, starting with the most controversial ones.

To start, install `praw` by entering `pip install praw` into your command line. I am assuming you are on Linux (specifically Debian).

Then, clone this repository (or just accountscrubber) to a location on your system, and edit it to include your username, password, and developer key info from https://www.reddit.com/prefs/apps/.

If you are running into lots of weird glitches, make sure your system's encoding is set to UTF-8. This is especially important when working with web applications like Reddit.
