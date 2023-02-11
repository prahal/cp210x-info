# cp210x-info
Get cp210x chipset info

Depends on python3-usb, on Debian:
`apt install python3-usb`

Requires privileges to the access usb device.

Example:
```
sudo ./cp210x-info.py --vid 0x10c4 --pid 0xea60
==================
CP2104
==================
CP2101N
Revision: A01
Firmware version: 1.0.4
```
