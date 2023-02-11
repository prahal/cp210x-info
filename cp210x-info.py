#!/usr/bin/python3

# Based on Craig Shelley (craig@microtron.org.uk) cp210x Linux kernel module
# driver code.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
import usb.core
import usb.util

class Cp210xInfo:
    # 1.0.2     A01
    # 1.0.4     A01
    # 1.0.8     A02

    PARTNUM_CP2101 = 0x01
    PARTNUM_CP2102 = 0x02
    PARTNUM_CP2103 = 0x03
    PARTNUM_CP2104 = 0x04
    PARTNUM_CP2105 = 0x05
    PARTNUM_CP2108 = 0x08
    PARTNUM_CP2102N_QFN28 = 0x20
    PARTNUM_CP2102N_QFN24 = 0x21
    PARTNUM_CP2102N_QFN20 = 0x22
    PARTNUM_UNKNOWN = 0xFF

    class FwVersion:
        def __init__(self, major, minor, build):
            self.major = major
            self.minor = minor
            self.build = build
    
    def has_fwversion(self):
        if (self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN28 or
        self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN24 or
        self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN20):
            return True
        return False


    def print_description(self):
        if self.partnum == Cp210xInfo.PARTNUM_CP2101:
            print("CP2101")
        if self.partnum == Cp210xInfo.PARTNUM_CP2102:
            print("CP2102")
        if self.partnum == Cp210xInfo.PARTNUM_CP2103:
            print("CP2103")
        if self.partnum == Cp210xInfo.PARTNUM_CP2104:
            print("CP2104")
        if self.partnum == Cp210xInfo.PARTNUM_CP2105:
            print("CP2105")
        if self.partnum == Cp210xInfo.PARTNUM_CP2108:
            print("CP2108")
        if (self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN28 or
        self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN24 or
        self.partnum == Cp210xInfo.PARTNUM_CP2102N_QFN20):
            print("CP2101N")
            if self.fwversion.major == 1 and self.fwversion.minor == 0:
                if self.fwversion.build < 8:
                    print("Revision: A01")
                elif self.fwversion.build == 8:
                    print("Revision: A02")
            print(f"Firmware version: " \
                  f"{self.fwversion.major}.{self.fwversion.minor}.{self.fwversion.build}")
        if self.partnum == Cp210xInfo.PARTNUM_UNKNOWN:
            print("Unknown CP210x")

class Cp210xUsbDevice:
    REQTYPE_DEVICE_TO_HOST = 0xc0
    CP210X_VENDOR_SPECIFIC = 0xFF
    CP210X_GET_PARTNUM = 0x370B
    CP2102N_GET_FW_VERS = 0x0010

    def __init__(self, usb_device):
        self.device = usb_device

    def get_info(self):
        cp210x_info = Cp210xInfo()

        interface = device[0].interfaces()[0]

        ret = device.ctrl_transfer(Cp210xUsbDevice.REQTYPE_DEVICE_TO_HOST,
                                   Cp210xUsbDevice.CP210X_VENDOR_SPECIFIC,
                                   Cp210xUsbDevice.CP210X_GET_PARTNUM,
                                   interface.bInterfaceNumber, 1);
        cp210x_info.partnum = ret.pop()

        if cp210x_info.has_fwversion():
            ret = device.ctrl_transfer(Cp210xUsbDevice.REQTYPE_DEVICE_TO_HOST,
                                   Cp210xUsbDevice.CP210X_VENDOR_SPECIFIC,
                                   Cp210xUsbDevice.CP2102N_GET_FW_VERS,
                                   interface.bInterfaceNumber, 3);
            cp210x_info.fwversion = Cp210xInfo.FwVersion(ret[0], ret[1], ret[2])

        return cp210x_info


cp210x_infos = []

parser = argparse.ArgumentParser()
parser.add_argument('--vid', type=str,
                   help='USB device vendor ID')
parser.add_argument('--pid', type=str,
                   help='USB device product ID')
args= parser.parse_args()

vendor_id = int(args.vid, 16)
product_id = int(args.pid, 16)

devices = usb.core.find(find_all=True, idVendor=vendor_id, idProduct=product_id)
if devices is None:
    raise RuntimeError('Device not found')

for device in devices:
    cp210x_dev = Cp210xUsbDevice(device)
    cp210x_info = cp210x_dev.get_info()
    cp210x_infos.append(cp210x_info)

for cp210x_info in cp210x_infos:
    print("==================")
    cp210x_info.print_description()
