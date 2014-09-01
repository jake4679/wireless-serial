#!/usr/bin/env python

import os
import os.path
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpi_serial.settings")

    from serial_configuration.models import SerialPort

    try:
        # Create 2 new serial ports and save them off
        port = SerialPort(device_file='/dev/ttyUSB0')

        port.save()
    
        port = SerialPort(device_file='/dev/ttyAMA0')

        port.save()
    except Exception as e:
      print e
