# potato

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  [![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)  [![Made With:PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-red)](https://pypi.org/project/PyQt5/)

<img src="https://github.com/mbridak/potato/raw/main/pic/potato.png" width="100"/>
Pulls latest POTA spots. Displays them in a compact interface. If you have an instance of `flrig` running, when you click on a spot your radio will automatically tune to the spotted frequency and change modes to match the spot.   Filter output to band and or mode. If you double click on a spot(s), spots from that activator will be highlighted green. You can use this keep track of who you have worked. Activators can be toggled off again by double clicking the activator a second time. 

## Changes since 21.9.14 Latka

I ditched using the rigctld daemon supplied by hamlib tools. Instead I'll be using the [flrig's](http://w1hkj.com/files/flrig/) XmlRPC interface. It's way simpler. It's available on all platforms.

For Debian based Linux or Raspberry OS you can:

`sudo apt install flrig`

Merged PR from [jon-laudner](https://github.com/jon-laudner) changing the API address since the legacy one was deprecated.

Merged PR from [adammelancon](https://github.com/adammelancon). Added a check to see if flrig is running, to prevent UI freeze on Windows.

Added a double click to highlight spots from an activator(s). 

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
 