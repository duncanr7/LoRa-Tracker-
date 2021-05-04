# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import busio
import digitalio
import board
import struct

import adafruit_gps
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# Board LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

RX = board.D0
TX = board.D1

uart = busio.UART(TX, RX, baudrate=9600, timeout=100)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Feather M0 RFM9x Pinouts
cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([]) # input data from TTN network 

# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([]) # input data from TTN network 

# TTN Application Key, 16 Bytess, MSB
app = bytearray([]) # input data from TTN network 

ttn_config = TTN(devaddr, nwkey, app, country="US")

lora = TinyLoRa(spi, cs, irq, rst, ttn_config)
last_print = time.monotonic()
# Data Packet to send to TTN
data = bytearray(8)
while True:
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current

        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
            # Encode payload as bytes
        lat = int(gps.latitude * 1000000)
        long = int(gps.longitude * -1000000)

        data[0] = (lat >> 24) & 0xFF
        data[1] = (lat >> 16) & 0xFF
        data[2] = (lat >> 8) & 0xFF
        data[3] = (lat >> 0) & 0xFF

        data[4] = (long >> 24) & 0xFF
        data[5] = (long >> 16) & 0xFF
        data[6] = (long >> 8) & 0xFF
        data[7] = (long >> 0) & 0xFF

        time.sleep(2)
         #Send data packet
        lora.send_data(data, len(data), lora.frame_counter)
        print("Packet Sent!")
        led.value = True
        lora.frame_counter += 1
        time.sleep(2)
        led.value = False
