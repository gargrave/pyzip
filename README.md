# PyZip

PyZip is a small interactive Python command-line tool that I built a while back to help me manage frequent sets of backups/archives using 7zip on both Windows and Mac systems.

Basically, it stores a list of "projects," which are essentially just directories that you want to be able to archive frequently. When you launch the utility, it will give you a list of all of your existing projects, so you can quickly create (and optionally make a copy of) backup archives of those. They can also be categorized, and you can add/remove projects from the CLI as well (or just edit the JSON config file manually, if you prefer). It might seem like an odd workflow, but it fulfilled a specific use-case I had at the time, and it did its job handsomely.

The command line interactions are all coded manually, so the code is probably a lot more verbose than it would be if I had used a library for it, but it was a good learning experience (i.e. "don't code an interactive CLI from scratch").

## Notes

Note that this does make a few assumptions about your system. While it would be easy enough for anyone with a basic knowledge of Python to update, it is currently hard-coded around these assumptions:

- You are on either a Windows or OSX system (Linux support should be easy enough, but it would require a few new lines of code).
- You have 7zip installed in a specific place:
  - On Win, it assumes the default 7zip package was installed at: `C:\Program Files\7-Zip\7z.exe`
  - On Mac, it assumes you have the free Keka app installed, in which case the 7zip executable would be located at: `/Applications/Keka.app/Contents/Resources/keka7z`
  - These paths are easily changeable, in `app/commands/command_builder.py`, lines 39-42.
- The config file is created at `[User Documents]\PyzipConfig.json`. I feel like it's a pretty sensible spot, but you can always manually change it in `app/config.py`, lines 8-9.