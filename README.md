# SHOW LIST (OFFICIAL NAME IN PROGRESS)

## Table of Contents

- [About the Program](https://github.com/MarkE16/ShowList#about-the-program)
- [Program Version](https://github.com/MarkE16/ShowList#program-version)
- [Changelog](https://github.com/MarkE16/ShowList#changelog)
- [How to Use](https://github.com/MarkE16/ShowList#how-to-use)
- [Updating](https://github.com/MarkE16/ShowList#updating)
- [Authentication](https://github.com/MarkE16/ShowList#authentication)
- [Report A Bug](https://github.com/MarkE16/ShowList#report-a-bug)

## About The Program

This is a console-based program designed to sort out and hold your list of shows/movies that you're watching. It may soon be transformed to a GUI, but that's not decided yet.

## Program Version

This program is currently in version 1.4. More updates will come soon for features, bug fixes, and/or improvements.

## Changelog

The following is the changes this program went through. Take a look!
> **Version 1.4** | ??? | *FEATURE UPDATE*
> - Clover removed. :(
> - Removed the 'Episode' section for ShowsToWatch
> - Added more status options to choose from, allowing you to change the status for the title you're on.
> - Moved 'About The Program' to Settings.
> - Allowed the ability to remove titles from your upcoming and completed lists.
> - Added the ability to check for updates, useful to know when the next version comes out! (Make sure to be connected to the internet of course).
> - Fixed a problem where data didn't save when deleting an account.
> - Added the 'kind' option to view what type of show it is (TV, Movie), allowing different info to appear.
> - Fixed the checklist whether a title is in a list or not when viewing title info.
> - Added a new option to settings (PLEASE READ ON HOW TO PROPERLY UPDATE THE DATA.PY FILE IF USING A OLDER VERSION AS 1.4 COULD BREAK IF OLD DATA IS NOT UPDATED BY GOING TO '1.4 Release Notes' IN 'Releases'. IF STARTING FROM 1.4, YOU ARE GOOD).
> - Code improvements have been made.
> - Made the console UI look more cleaner and user-friendly.
>
> **Version 1.3.1** | 12.8.2021 | *BUG FIX/IMPROVEMENT UPDATE*
> - Fixed error messages that shouldn't have appeared when doing certain actions.
> - When viewing show information, you will now be able to see whether the show is either one of your lists (currently, it will only show when there is at least one show in each list, otherwise it'll show something else. This will be fixed in an upcoming update.)
> - You no longer have to enter the entire show's name just to view information when in 'Menu > Shows to Watch'.
> - You can now back out on creating an account.
>
> **Version 1.3** | 11.17.2021 | *FEATURE UPDATE*
> - Added an account system! Now you can manage many shows between other users without messing anything up.
> - Guest Mode. This feature is just the normal program but it doesn't save data.
> - Improvements were made.
> - Looked high and low for sneaky bugs, they were removed.
>
> **Version 1.2** | 11.12.2021 | *FEATURE UPDATE*
> - Added a piece of information to shows called 'Status', allowing you to see whether if you're watching a show, or if completed with it.
> - Made some minor changes.
> - Squashed some bugs.
>
> **Version 1.1** | 11.6.2021 | *FEATURE UPDATE*
> - Replaced the option "Add a show" with "Search show", allowing the user to find shows instead of typing in the name.
> - Made some improvements.
>
> **Version 1.0** | 10.23.2021 | *PROGRAM RELEASE*
> - Initial Release.

## How to Use
1. Download the files, all you'll really need though is 'main.py'.
2. Extract the zip folder, so you can access the contents.
3. Run 'main.py'. A 'data.py' file should automatically be created, if not, add one in the same folder as 'main.py'.

## Updating
As of now, you cannot update the program by adding new contents to the current file you're updating, you are required to download a newer version of the program if you're updating. This can cause problems with not having your save data carried over to the latest version. Here's what you'll need to do to transfer your save data.
1. Download the latest version of the application, extract the contents, blahblahblah.
2. Go into your old version of the program with the save data you want to transfer by locating the **data.py** file.
3. Copy the **data.py** file.
4. Locate the folder for the latest version, then paste the file into the folder (if there is a data.py file already in there, paste anyway to replace the old one. Make sure it's called 'data.py' and not 'data - Copy.py', or something like that).
5. If done correctly, you should have your save data in the latest version.

## Authentication
This program uses the PyGithub library to fetch information from this repo such as fetching the latest version for checking updates. By doing so, it uses up the rate limit of the API. The limit for non-authenticated users is 60 requests per hour, but the limit for authenticated users is much higher with 5000 requests per hour. A smaller rate limit can be somewhat bad as reaching the limit will crash the program. If you don't care about the rate limit, you do not have to be authenticated (just don't check for updates a lot). If you do, you can follow the instructions below:
1. Go into the program's files, and find the file 'auth.py'. If it doesn't exist, create it.
2. In the file, add the following code:
```py
TOKEN: str = "TOKEN"
```
- The file is ready, now you just need your token.  
3. Go to Github > Settings > Developer Settings > Personal access tokens.  
4. Create your token (customize the settings for your token however you like).  
5. Copy the token, then go back to 'auth.py' and paste 'TOKEN' with your token.
- You should now be authenticated!

## Report A Bug
This project is still new and in development, so bugs are likely to appear. If you do find youself encountering a bug, please report it here using the following format:

### Title (A small description of the bug)

### Platform on where you're running the program (Windows, Linux, MacOS, etc.)

- [x] Windows
- [ ] Linux
- [ ] MacOS

### What version of the program are you using?
-> Please include the version number of where the bug was produced, that way it is easier to find the bug. Latest version to use is 1.4.

### Steps to reproduce the bug
-> Please include the steps on how you encountered the bug.