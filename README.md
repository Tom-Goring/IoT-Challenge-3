# IoT-Challenge-3
Assignment featuring Bluetooth or Radio transmission regarding a BBC:Microbit

### Prerequisites

This project will likely only run on linux.
In order to run the project you will first need to have the required libraries installed.
The main BLE library for Python used is BlueZero, which can either be built from source at:


`https://github.com/ukBaz/python-bluezero` 

or downloaded and installed with pip: 

`pip install Bluezero`

You will then need to pair your Microbit with whatever method you wish. I use bluetoothctl 
in Linux'x shell.

In addition to the BLE library, you will also need to have both tkinter
and matplotlib installed and ready to be used. Guides on installation can be found 
online in multiple locations.

### Deployment

Once the prerequisite software has been installed and the Microbit has been paired, you will need to
download the source files by cloning the project. In GUI.py you will need to enter the address of both
your client machine (your desktop or laptop) and the Microbit. Both of these addresses can be located
by using bluetoothctl and using the command `show` for the client machine, and `paired devices` for the
Microbit.

After the correct addresses have been inputted, the program should be runnable.

### Functionality

The program offers accelerometer readings mapped to a graph, control of
the LED's on the MicroBit, the ability to send messages to display on
the bit, a temperature reading, and a graphical button display for when
the bit's buttons are held.