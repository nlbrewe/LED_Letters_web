#!/usr/bin/python3
#runneopixel.cgi
import subprocess
import cgi
import cgitb
import time
import sys
import signal


if __name__ == '__main__':
#input args:/usr/lib/cgi-bin/autooff.py,timeval(seconds)
#                                 0         1
    try:
        delay_time = int(sys.argv[1])
        time.sleep(delay_time)
        subprocess.run(['sudo','pkill','-2','-f','python3 /usr/lib/cgi-bin/setcolor.py'])
        print('<p>autooff stopped display.</p>')
    except:
        print('<p>Sorry, autooff failed.</p>')