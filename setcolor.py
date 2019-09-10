#!/usr/bin/python3
# Simple test for NeoPixels on Raspberry Pi

#setcolor.py

import time
import board
import neopixel
import sys
import signal

try:
    print ("setcolor start - " + time.strftime("%H:%M:%S"))
    #setcolor Number of arguments:7
    #input args:/usr/lib/cgi-bin/setcolor.py,pattern,color,animation,speed,length,brite,shutoff

    ##f = open("/home/pi/nlb.log",'w')  # write in text mode
    ##f.write("setcolor Number of arguments::{0}\n".format(len(sys.argv)))
    ##f.write("progname,pattern,color,animation,speed,length:{0},{1},{2},{3},{4},{5},{6},{7}\n"
    ##        .format(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],
    ##        sys.argv[6],sys.argv[7]))
    ##f.close()

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels = 99

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB
    oabrite=float(int(sys.argv[6]))/100
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=oabrite, auto_write=False,
                               pixel_order=ORDER)
except:
    print('<p>Failed to initialize neopixel.Neopixel</p>')

def colorWipe(pixels, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range( num_pixels ):
        pixels[i]= color
        pixels.show()
        time.sleep(wait_ms/1000.0)


def revColorWipe(pixels, color, wait_ms=10):
    """Reverses Wipe color across display a pixel at a time."""
    for i in range( num_pixels-1,-1,-1 ):
        pixels[i] = ((0,0,0))
        pixels.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(pixels, color, wait_ms=50, iterations=5):
    """Movie theater light style chaser animation."""
    if iterations > 0:   #0 indicates forever
        for j in range(iterations):
            for q in range(3):
                for i in range(0, num_pixels, 3):
                    pixels[i+q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, num_pixels, 3):
                    pixels[i+q] = 0,0,0
    else:
        while True:  #iterate forever
            for q in range(3):
                for i in range(0, num_pixels, 3):
                    pixels[i+q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, num_pixels, 3):
                    pixels[i+q] = 0,0,0

def scanner(pixels, color, wait_ms=50, iterations=2,length=4):
    """moving group of pixels traverse string and return."""
    if iterations > 0:   #0 indicates forever
        for j in range(iterations):
            for i in range(0, num_pixels-(length-1), 1):
                for q in range(length):
                    pixels[i+q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                if i < num_pixels-length:
                    pixels[i] = 0,0,0
            for i in range((num_pixels-1),(length-1),-1):
                for q in range(length):
                    pixels[i-q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                if i > length:
                    pixels[i] = 0,0,0
    else:
        while True:  #iterate forever
            for i in range(0, num_pixels-(length-1), 1):
                for q in range(length):
                    pixels[i+q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                if i < num_pixels-length:
                    pixels[i] = 0,0,0
            for i in range((num_pixels-1),(length-1),-1):
                for q in range(length):
                    pixels[i-q] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                if i > length:
                    pixels[i] = 0,0,0

def rotate(pixels, color, wait_ms=50, iterations=2,length=4):
    """moving group of pixels traverse string and restart at beginning."""
    if iterations > 0:   #0 indicates forever
        for j in range(iterations):
            for i in range(0, num_pixels, 1):
                for q in range(length):
                    k=i+q
                    if k > num_pixels-1:
                        k=k-num_pixels
                    pixels[k] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                pixels[i] = 0,0,0
    else:
        while True:  #iterate forever
            for i in range(0, num_pixels, 1):
                for q in range(length):
                    k=i+q
                    if k > num_pixels-1:
                        k=k-num_pixels
                    pixels[k] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                pixels[i] = 0,0,0

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rainbow(pixels,brightness=1.0):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for i in range(num_pixels):
        pixels[i]= (int(float(wheel((int(i * 256 / num_pixels)) & 255)[0])*brightness),int(float(wheel((int(i * 256 / num_pixels)) & 255)[1])*brightness),int(float(wheel((int(i * 256 / num_pixels)) & 255)[2])*brightness))
    pixels.show()

def rainbowCycle(pixels, wait_ms=20, iterations=2):
    """Draw rainbow that uniformly distributes itself across all pixels, and moves."""
    if iterations > 0:   #0 indicates forever
        for j in range(256*iterations):
            for i in range(num_pixels):
                pixels[i]= wheel((int(i * 256 / num_pixels) + j) & 255)
            pixels.show()
            time.sleep(wait_ms/1000.0)
    else:
        while True:
            for j in range(256):
                for i in range(num_pixels):
                    pixels[i]= wheel((int(i * 256 / num_pixels) + j) & 255)
                pixels.show()
                time.sleep(wait_ms/1000.0)

def rainbowCyclePulse(pixels,wait_ms=5,span=1):
    """Draw rainbow that uniformly distributes itself across all pixels, moves, and pulses up and down in intensity."""
    while True:  #do forever
        for j in range(256):  #j moves color wheel position for starting pixel this cycle
            for k in range(0,100,span):  #cycle brightness up
                brightness=float(k)/100
                for i in range(num_pixels):  #iterate over all pixels
                    thispixelcolor=wheel((int(i * 256 / num_pixels) + j) & 255)
                    pixels[i]= (int(float(thispixelcolor[0])*brightness),int(float(thispixelcolor[1])*brightness),int(float(thispixelcolor[2])*brightness))
                pixels.show()
                time.sleep(wait_ms/1000)
            for k in range(100,-1,-1*span):  #cycle brightness down
                brightness=float(k)/100
                for i in range(num_pixels):  #iterate over all pixels
                    thispixelcolor=wheel((int(i * 256 / num_pixels) + j) & 255)
                    pixels[i]= (int(float(thispixelcolor[0])*brightness),int(float(thispixelcolor[1])*brightness),int(float(thispixelcolor[2])*brightness))
                pixels.show()
                time.sleep(wait_ms/1000)

def solidPulse(pixels,wait_ms=5,span=1,solidcolor="ff0000"):
    """Draw rainbow that uniformly distributes itself across all pixels, moves, and pulses up and down in intensity."""
    while True:  #do forever
        for k in range(0,100,span):  #cycle brightness up
            brightness=float(k)/100
            for i in range(num_pixels):  #iterate over all pixels
                thispixelcolor=solidcolor
                pixels[i]= (int(float(thispixelcolor[0])*brightness),int(float(thispixelcolor[1])*brightness),int(float(thispixelcolor[2])*brightness))
            pixels.show()
            time.sleep(wait_ms/1000)
        for k in range(100,-1,-1*span):  #cycle brightness down
            brightness=float(k)/100
            for i in range(num_pixels):  #iterate over all pixels
                thispixelcolor=solidcolor
                pixels[i]= (int(float(thispixelcolor[0])*brightness),int(float(thispixelcolor[1])*brightness),int(float(thispixelcolor[2])*brightness))
            pixels.show()
            time.sleep(wait_ms/1000)

def theaterChaseRainbow(pixels, wait_ms=50, iterations=2):
    """Rainbow movie theater light style chaser animation."""
    if iterations > 0:   #0 indicates forever
        for j in range(256*iterations):
            for q in range(3):
                for i in range(0, num_pixels, 3):
                    pixels[i+q] = wheel((i+j) % 255)
                pixels.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, num_pixels, 3):
                    pixels[i+q]= 0,0,0
    else:
        while True:
            for j in range(256):
                for q in range(3):
                    for i in range(0, num_pixels, 3):
                        pixels[i+q] = wheel((i+j) % 255)
                    pixels.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(0, num_pixels, 3):
                        pixels[i+q]= 0,0,0

# Main program logic follows:
if __name__ == '__main__':
#input args:/usr/lib/cgi-bin/setcolor.py,pattern,color,animation,speed,length,brite,timeout
#                                 0         1      2       3       4      5      6     7
#color can be (r,g,b) tupple or 'rainbow' or 'off'
##    print('<p>entering setcolor.py</p>')
    try:
        splitarg = sys.argv[2].split(',')
        red = int(splitarg[0])
        green = int(splitarg[1])
        blue = int(splitarg[2])
        color = int(red),int(green),int(blue)
        animation_wait_ms=(100-int(sys.argv[4]))  #animation speed

    except KeyboardInterrupt:
        pixels.fill((0,0,0))
        pixels.show()

    if sys.argv[1] == 'rainbow': #pattern = 'rainbow'
        print('<p>pattern = rainbow, calling rainbow().</p>')
        try:
            rainbow(pixels,brightness=1.0)
        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()

    elif sys.argv[1] == 'off':  #if off, reinit neopixel string
        print('<p>setcolor pattern = off, reinitializing neopixel.NeoPixel.</p>')
        try:
            pixels.deinit()
            pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=oabrite, auto_write=False,
                           pixel_order=ORDER)
        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()

    elif sys.argv[1] == 'solid':     #pattern='solid'
        message = '<p>setcolor pattern = solid, calling pixels.fill({})'.format(color) + '</p>'
        print(message)
        try:
            pixels.fill((color))
            pixels.show()

        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()

    if sys.argv[3] == 'none' or sys.argv[1] == 'off':  #if no animation, nothing more to do
        print('<p>animation = none or pattern = off.</p>')
        try:
            pass
        except KeyboardInterrupt:
            print('<p>setcolor animation = none, exception taken.</p>')

    else:
        if sys.argv[3] == 'theater':
            try:
                if sys.argv[1] == 'rainbow':
                    theaterChaseRainbow(pixels, wait_ms=animation_wait_ms,iterations=0)
                else:  #pattern = 'solid'
                    theaterChase(pixels, color, wait_ms=animation_wait_ms,iterations=0)
            except KeyboardInterrupt:
                pixels.fill(0,0,0)
                pixels.show()

        elif sys.argv[3] == 'pulse':
            if sys.argv[1] == 'rainbow':
                try:
                    if int(sys.argv[4]) < 90:
                        pulsespan = 1
                    else:
                        pulsespan= max(int(10-animation_wait_ms),1)
                    rainbowCyclePulse(pixels,wait_ms=animation_wait_ms,span=pulsespan)
                except KeyboardInterrupt:
                    pixels.fill((0,0,0))
                    pixels.show()
            else:
                try:
                    if int(sys.argv[4]) < 90:
                        pulsespan = 1
                    else:
                        pulsespan= max(int(10-animation_wait_ms),1)
                    solidPulse(pixels,wait_ms=animation_wait_ms,span=pulsespan,solidcolor=color)
                except KeyboardInterrupt:
                    pixels.fill((0,0,0))
                    pixels.show()

        elif sys.argv[3] == 'rotate':
            try:
                packlen=int((int(sys.argv[5])*num_pixels)/100)
                pixels.fill((0,0,0))
                pixels.show()
                rotate(pixels, color, wait_ms=animation_wait_ms, iterations=0,length=packlen)
            except KeyboardInterrupt:
                pixels.fill((0,0,0))
                pixels.show()

        elif sys.argv[3] == 'scanner':
            try:
                packlen=int((int(sys.argv[5])*num_pixels)/100)
                pixels.fill((0,0,0))
                pixels.show()
                scanner(pixels, color, wait_ms=animation_wait_ms, iterations=0,length=packlen)
            except KeyboardInterrupt:
                pixels.fill((0,0,0))
                pixels.show()

        elif sys.argv[3] == 'rainbow_cycle':
            try:
                rainbowCycle(pixels,wait_ms=animation_wait_ms, iterations=0)
            except KeyboardInterrupt:
                pixels.fill((0,0,0))
                pixels.show()

        elif sys.argv[3] == 'demo':
            try:
                while True:
                    colorWipe(pixels, (255, 0, 0),wait_ms=animation_wait_ms)  # Red wipe
                    colorWipe(pixels, (0, 255, 0),wait_ms=animation_wait_ms)  # Blue wipe
                    colorWipe(pixels, (0, 0, 255),wait_ms=animation_wait_ms)  # Green wipe
                    rotate(pixels,(0,0,255),wait_ms=animation_wait_ms)
                    rotate(pixels,(255,255,255),wait_ms=animation_wait_ms)
                    rotate(pixels,(0,255,0),wait_ms=animation_wait_ms)
                    revColorWipe(pixels,(0,0,255),wait_ms=animation_wait_ms)  # reverse green wipe
                    theaterChase(pixels, (127, 127, 127),wait_ms=animation_wait_ms)  # White theater chase
                    theaterChase(pixels, (127,   0,   0),wait_ms=animation_wait_ms)  # Red theater chase
                    theaterChase(pixels, (  0,   0, 127),wait_ms=animation_wait_ms)  # Blue theater chase
                    theaterChase(pixels, (  0,   127, 0),wait_ms=animation_wait_ms)  # Green theater chase
                    rainbow(pixels)
                    rainbowCycle(pixels,wait_ms=animation_wait_ms)
                    theaterChaseRainbow(pixels,wait_ms=animation_wait_ms)
                    scanner(pixels,(0,0,255),wait_ms=animation_wait_ms)
                    scanner(pixels,(255,0,255),wait_ms=animation_wait_ms)
                    scanner(pixels,(0,255,255),wait_ms=animation_wait_ms)

            except KeyboardInterrupt:
                colorWipe(pixels, (0,0,0), wait_ms=0)

    print('<p>setcolor animation finished, exiting setcolor.py.</p>')
    print ("setcolor exit - " + time.strftime("%H:%M:%S"))
