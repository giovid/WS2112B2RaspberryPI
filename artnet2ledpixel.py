import sys
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,
                    SO_BROADCAST)

# Simple test for NeoPixels on Raspberry Pi
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1024

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False,
                           pixel_order=ORDER)

UDP_IP = ""
UDP_PORT = 6454


def send_led(universe, dmx):
    first_pixel = universe * 170
    end_pixel = first_pixel + 170
    i = 0
    while first_pixel < end_pixel:
        pixels[first_pixel] = dmx[i]
        first_pixel += 1
        i += 1
    pixels.show()


def ragruppa(dmx):
    lista = []
    i = 0
    while i < 510:
        lista.append((dmx[i], dmx[i + 1], dmx[i + 2]))
        i += 3
    return lista


def listen_and_redirect_artnet_packets():
    sock = socket(AF_INET, SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    sock_broadcast = socket(AF_INET, SOCK_DGRAM)
    sock_broadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock_broadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if (sys.getsizeof(data) > 540):
                list_dmx = list(data)
                universe = list_dmx[14]
                list_dmx = list_dmx[18:]
                send_led(universe, ragruppa(list_dmx))


        except KeyboardInterrupt:
            sock.close()
            sock_broadcast.close()
            sys.exit()


listen_and_redirect_artnet_packets()
