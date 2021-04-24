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
devaddr = bytearray([0x26, 0x02, 0x19, 0xA0])

# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([0xBE, 0xC6, 0x42, 0x1A, 0x95, 0xD8, 0x14, 0xC3, 0xC0, 0x32, 0xCB, 0xF7, 0xFC, 0x6C, 0xF9, 0x7A])

# TTN Application Key, 16 Bytess, MSB
app = bytearray([0xDF, 0xA3, 0x7C, 0x56, 0x8F, 0x3E, 0xDF, 0x5D, 0xC3, 0xDE, 0x6F, 0x7D, 0x59, 0x8F, 0x51, 0x05 ])

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
