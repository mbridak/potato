# potato

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  [![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)  [![Made With:PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-red)](https://pypi.org/project/PyQt5/)

<img src="https://github.com/mbridak/potato/raw/main/pic/potato.png" width="100"/>
Pulls latest POTA spots. Displays them in a compact interface. If you have an instance of flrig or rigctld running, when you click on a spot your radio will automatically tune to the spotted frequency and change modes to match the spot.   Filter output to band and or mode. If you double click on a spot(s), spots from that activator will be highlighted green, and be added to the clipboard. You can use this keep track of who you have worked. Activators can be toggled off again by double clicking the activator a second time.

## Changes since 22.2.19 Instant Mashed

Command line options for selecting CAT backend:

```bash
potato.py --rigctld localhost:4532

or

potato.py --flrig localhost:12345
```

Text entry field added to top of the window to filter the spots returned.
For example:

- `US-WA` will show only the parks in US Washington State.
- `-US-WA` will exclude all parks in US Washington State.

More spot information was added to each line.

## Running from source

First install the requirements.

`python3 -m pip3 install -r requirements.txt`

Or if you're the Ubuntu/Debian type you can:

`sudo apt install python3-pyqt5 python3-requests python3-psutil`

Then, run the program from source.

`python3 potato.py`

![screenshot](pic/screenshot.png)

## Building a binary executable

I've included a .spec file in case you wished to create your own binary from the source. To use it, first install pyinstaller.

`python3 -m pip3 install pyinstaller`

Then build the binary.

`pyinstaller -F potato.spec`

Look in the newly created dist directory to find your binary.

Or execute the install.sh shell script in the install_icon folder to copy the binary from the dist directory to your ~/.local/bin folder and install a launcher icon.
