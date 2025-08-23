
## What is Naughty archiver 2000
It's a gallery-dl wrapper built in Python to help managing users, cookies, statistics, handle extraction errors and much more

Gallery-dl is made my mikf at https://github.com/mikf/gallery-dl

This program is dedicated to data hoarders and archivers
Here's the list of features:

 - Implemented extractors are customized so that they are easier to setup and run
 - User manager with custom options for each user
 - Cookie manager to switch between accounts
 - Logging of statistics and files downloaded
 - Optional popups for warnings
 - Tray icon for easy access to options and operations
 - Easily creatable custom extractors	

See changelogs.txt for more features

Because every extractor has it's own options and it's customized based on gallery-dl, there's only a few already implemented, most gallery-dl settings are also predetermined, such as file names (although still easily modifiable from source).

NA2000 is meant to be run in the background mind-free and can be forcefully terminated at any time
<img width="906" height="646" alt="NA2000" src="https://github.com/user-attachments/assets/76e101a2-3283-4fbe-83bb-37e870ac690c" />
<img width="1293" height="392" alt="NA2000" src="https://github.com/user-attachments/assets/a7fd3fc4-5a82-4e38-9696-ed528408d9b4" />
<img width="588" height="445" alt="NA2000" src="https://github.com/user-attachments/assets/750c72c5-8370-4fff-a8f8-5e8c1f833ca7" />

## How to report issues
Please report any bugs or changes you wish, some extractors weren't tested fully
Before reporting any issue:
 - Check if there's a new version of [gallery-dl](https://github.com/mikf/gallery-dl), replace gallery-dl.exe with the new version a try again
 - Append debug logs by starting the app with the --debug flag
 
Almost every exception will be fully written in `saved/latestException.txt`

Report issues in this repository if:
 - The program crashes
 - Any error/malfunction happens outside of the console logger widget
 - Gallery-dl throws a keyerror exception in the console
 - Gallery-dl crashes or doesn't start
 
Report issues in [gallery-dl](https://github.com/mikf/gallery-dl) repository if:
 - There's API errors that don't progress the extraction

Errors that begin with '[g-dl]' in the console are from the gallery-dl process
The configuration files passed in gallery-dl are found in `./external/`

## How to install
This is a windows only software for now
Download the and run the exe file or download the repo and run the following commands (Python 3.10+)

    pip install -r requirements.txt
    python na2000.py
 
The program will be ready to use, it can only run one instance at a time per folder
## How to use
### First time
On first launch you only have two tabs: statistics and General
General is the broth in your ramen, everything else is ingredients, you should notice in the bottom of the window 'Console' and 'Settings', here you can set custom values for various settings.
- Hover over them to see an explanation
- Click on the button that says 'download tools', this will download  - Gallery-dl, FFMPEG, Mkvmerge
- Now you decide which extractor you want to have, in the dropdown select it and click insert extractor, a new tab will appear

### Save data & updates
Data is stored in the same directory as na2000.exe, making it a portable program, in a folder called `saved`<br/>Please do not delete any file outside the saved folder, do not modify or occupy files in `external`<br/>To update download the new version and drag the saved folder in there, or drag the new version onto the existing one<br/>If you want you can just update gallery-dl by replacing the exe inside `external`
### Arguments
NA2000 can be called with the following arguments:

    --hidden 	:	Runs NA2000 hidden in the tray (the window can still be brought up afterwards)
    --runall 	:	Upon launch NA2000 will start all enabled extractors automatically
    --debug		:	Debug information in saved/debug

To auto-start on boot press `Win + R`  and type `shell:startup` here create a batch file like the following, making sure you use the right python path

    "D:\PROGRAMS_X64\anaconda\envs\NA2000\python.exe" "D:\\NA 2000\na2000.py" --hidden --runall
 
### Extractors
Extractors are like robots that do the work for you, they extract media and information from specific websites.<br/>Settings, users and cookies between extractors aren't shared<br/>Select your extractor in the tabs above and take a look at the buttons and settings:
 - `Skip`: Skips the user it's currently extracting
 - `Run`: Force run the extractor (usually you run all extractors at once from the general tab)
 - `Users`: Manage the users for the extractor
 - `Cookies`: Manage your accounts for the extractor
 - `Errored`: See errored URLs (if functionality is present)
 - `Custom run`: Define single custom URLs to extract (select the type of url, type the argument and click insert)

What you first want to do is go in the extractor settings and set:
 - `default destination`: which is where the extraction of users with literal 'default' as destination will go in (folder named with the username).<br/>Useful for archiving many accounts to the same folder
 - `sleep`: How much to sleep between download and API requests (leaving it default is good)
Other extractors might have more settings, you can disable extractors without deleting them by unchecking the group box in the extractor settings

See extractors.md for more information about each extractor's options

### Users
Click on the 'users' button on the extractors and two tables will pop up:
 - **Bottom table:** used to insert your user data and preferences. <br/>Example: If we want to extract user 'shrimp' on twitter put 'shrimp' under User Handle, put C:/users/shrimp under 'destination path', select 'normal' as extraction level and check 'media' then we click 'insert' on the bottom right of the window. Now the user will be in the Top table and will be extracted first
 - **Top table:** Users already added for extraction, you can change the settings of the users immediately from the table. <br/>The operations you see on the bottom of the window are for this table and will operate of selected users (most left checkbox selected)

To save the table for the extractor press the bottom left button with a writing icon, hover for tooltips
### Cookies
Set your cookies by pressing the cookies button on the extractor
Create a new file by putting a filename, clicking '+' and follow the instructions on the textboxes then click 'Use this one!'
The cookies must be NETSCAPE formatted

###	Running extractor & logging
Go to the General tab and press 'Run all', this will run all extractors enabled<br/>You will see output coming out on the console, you can hide or show verbose output with the button above 'debug'As an optimization NA2000 will keep track of the last time you've extracted each user, so that it can stop when it meets files it already goes through<br/>After every user of one extractor are done it will repeat the process again as many times as you define
 
 ## Creating a custom extractor
 You are sad that your favorite extractor is not there, I tried to make it as easy as possible to create a custom one, it will involve some easy coding 
 
For this example we will create a Bluesky extractor

### Download source code and create files
To add an extractor you should have downloaded the source code

These are the files that will be opened: `lib/extractors/extractorTemplate.py` `lib/ui/extractorsManager.py`

I recommend you make a bear bone extractor by first skipping what you don't understand and then slowly learn it off other extractors

### Setup the extractor settings
There is a template that will help you make an extractor
copy `lib/extractors/extractorTemplate.py` into `lib/extractors/bluesky.py`
Follow the steps indicated in the file

What you can personalize (non-logic):
 - `extractorName`
 - `commonUserOptions`
 - `argsAppend`
 - `filterAppend`
 - `cookiesTextBoxText`
 - Errored URLs list manager
 - The jobs/URLs that will be passed to gallery-dl
 - Cursor extraction and updating
 - Users options
 - URLs Definitions

What you should base off of necessity (logic):
 - `galleryExtractorName`
 - Configuration for the UI to the program's config
### Initializing your extractor
Open `lib/extractorsManager.py`
Import your extractor `from lib.extractors.bluesky import Bluesky`
Follow the instructions in the `__init__` method:
 - Add your extractor in `extractorFactories`

Now open the program, go in the general tab, settings, turn on `'Validate extractors on launch'` to help debug faster, insert your extraction and hope your settings went all good


### Debugging your extractor
Jobs are configuration files passed to gallery-dl like you would do with `.conf` files
<br/>If there's an annoying thing it's this: You need a filename for your extracted files but to know which keys and format to use you need metadata extracted from the extractor. <br/>What you should do is set the filename key to `temp.json`, and run an extraction, then save that file and base your filenames after the keys in there, alternatively run the url with the `-K` flag<br/>You can even call an module to decide the filename for you, like the extractors already present, very useful for dynamic filenames

## Useful classes 
You may edit these classes for your specific purpose 

`GalleryOutputHandler` Manages extractor events based on gallery-dl output, the pattern data gets fed from `outputHandlerCreator_manager`<br/><br/>`OutputEvents` List of events that can occur in `GalleryOutputHandler`<br/>`GalleryRunner` Class that starts a gallery-dl process<br/>`Logic.py` Base .conf file for gallery-dl (Before extractors override the settings) <br/>`Extractor` Main class that starts and setups an extractor, provides the already-made widgets and configuration<br/>`ExtractorManager` Does operations on all extractors<br/>`CrashHelper` Kills gallery-dl on sudden crashes<br/>`\external\logic*` Filenames of the extractors
 
Helper classes:
`QtHelper` `VarHelper` `Enums`

## Resources
- Every icon in lib/ui/ico by Microsoft
- Gallery-dl by mikf. This program is completely dependent on gallery-dl and as such every rule that applies to gallery-dl's license also applies to this program, code from this repository outside FFMPEG, MKVMERGE and GALLERY-DL, is considered part of original code.

Do not get discouraged by the program's name
Written in python as a learning vector
