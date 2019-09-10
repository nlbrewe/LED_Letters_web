#!/usr/bin/python3

#runneopixel.py

#called from html
import time
import subprocess
import cgi
import cgitb
import socket
import os

cgitb.enable()
input_data=cgi.FieldStorage()

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

print('Content-Type:text/html') #HTML is following
print()                          #Leave a blank line

print ("<p>runneopixel start - " + time.strftime("%H:%M:%S") + "</p>")

try:   #kill off any animation processes still running
##    print('<p>Stopping setcolor.py</p>')
    subprocess.run(['sudo','pkill','-2','-f','python3 /usr/lib/cgi-bin/setcolor.py'])
##    ,stdin=None,stdout=None,stderr=None,close_fds=True).pid
    print('<p>runneopixel.  Stopped setcolor processes</p>')
except:
    print('<p>runneopixel.  Error stopping setcolor processes</p>')

try:   #kill off any autooff processes still running
##    print('<p>Stopping autooff.py</p>')
    subprocess.run(['sudo','pkill','-2','-f','python3 /usr/lib/cgi-bin/autooff.py'])
    print('<p>runneopixel.  Stopped autooff processes</p>')
except:
    print('<p>runneopixel.  Error stopping autooff processes</p>')

ipaddress=os.popen("ifconfig wlan0 | grep 'inet ' ").read()
message = '<p>runneopixel.  wlan0 ip info: {0}'.format(ipaddress) + '</p>'
print(message)

#  handle autooff commands by launching the autooff.py script.  Popen runs the
#  autooff.py script but doesn't wait for it to return.  autooff.py waits for the
#  required time and then kills all setcolor.py scripts.
if input_data["shutoff"].value != 'manual':
    if input_data["shutoff"].value == '30_sec':
        delay=30
    elif input_data["shutoff"].value == '30_min':
        delay=1800
    elif input_data["shutoff"].value == '1_hr':
        delay=3600
    elif input_data["shutoff"].value == '2_hr':
        delay=7200
    else:
        delay=3600
    print('<p>Launching autooff.py</p>')
    pid=subprocess.Popen(['sudo','python3','/usr/lib/cgi-bin/autooff.py','{}'.format(delay)]
        ,stdin=None,stdout=None,stderr=None,close_fds=True).pid
    print('<p>runneopixel.  Launched autooff.py</p>')

time.sleep(0.1)

#  launch setcolor.py script.  Setcolor.py may go into a continuous loop or may
#  return once it finishes.  If it loops, it will be killed later
try:
    colorstr = '{0},{1},{2}'.format(*hex_to_rgb(input_data["npcolor"].value))
##    print('<p>Launching setcolor.py</p>')
    pid=subprocess.Popen(['sudo','python3','/usr/lib/cgi-bin/setcolor.py',
        input_data["pattern"].value,colorstr,input_data["animation"].value,
        input_data["speed"].value,input_data["length"].value,input_data["brite"].value,
        input_data["shutoff"].value],stdin=None,stdout=None,stderr=None,close_fds=True).pid

    print ('<p>runneopixel.  Launched setcolor.py at ' + time.strftime("%H:%M:%S") + '</p>')
except:
    print('<p>runneopixel.  Error launching setcolor.py at'  + time.strftime("%H:%M:%S") + '</p>')


