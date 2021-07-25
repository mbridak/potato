# potato

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  [![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)  [![Made With:PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-red)](https://pypi.org/project/PyQt5/)

<img src="https://github.com/mbridak/potato/raw/main/pic/potato.png" width="100">
Pulls latest POTA spots. Displays them in a compact interface. If you have an instance of `rigctld` running, when you click on a spot your radio will automatically tune to the spotted frequency and change modes to match the spot.   Filter output to band and or mode.
<br/>

If you use Linux you can try the binary [here](https://github.com/mbridak/potato/releases/download/21.5.23/potato).

Or, if you don't run the same version of Linux as the package is built against.

`python3 -m pip3 install -r requirements.txt`

Then, run the program from source.

`./potato.py`



![screenshot](https://github.com/mbridak/potato/raw/main/pic/screenshot.png)

## rigctld and default filter widths

For some reason rigctld changes the filter width when you set the mode. When you send a filter width of 0 rigctld sets the modes filter width to 'hamlibs backend default'. I'm not a big fan of their CW default, and found it rather annoying to have too change the filter on the radio after each click a spot. So I put back in the hard coded defaults. I'm not sure why we're not able to just change the mode and leave the filters alone.

In short untill I add a settings dialog to change the defaults you can change your own by editing the source.

        self.bw['LSB'] = '2400'
        self.bw['USB'] = '2400'
        self.bw['FM'] = '15000'
        self.bw['CW'] = '200'
        