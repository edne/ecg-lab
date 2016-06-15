#!/usr/bin/env python
from sys import argv
import serial
import matplotlib.pyplot as plt
import threading


user_stop = [False]


def get_user_stop(user_stop_ref):
    user_stop_ref[0] = raw_input().lower() == "stop"


def stopped():
    return user_stop[0]


def open_serial():
    serial_path = "/dev/ttyUSB1"  # Psoc5
    if argv[1:]:
        serial_path = argv[1]

    port = serial.Serial(serial_path, baudrate=115200,
                         rtscts=True, dsrdtr=True)
    return port


def plot(size):
    port = open_serial()
    plt.ion()
    ydata = [0] * size
    line, = plt.plot(ydata)
    plt.ylim([0, 255])

    try:
        while not stopped():
            ydata = [ord(x) for x in port.read(size)]

            line.set_xdata(range(len(ydata)))
            line.set_ydata(ydata)

            plt.draw()
            plt.pause(0.000001)
    except KeyboardInterrupt:
        port.close()


if __name__ == "__main__":
    thread = threading.Thread(target=get_user_stop, args=(user_stop,))
    thread.daemon = True
    thread.start()

    plot(256)
