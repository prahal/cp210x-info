# cp210x-info
Get Silicon Labs CP210x USB-to-UART bridge controllers Part number, CP2102N revision and firmware version.

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
