#!/usr/bin/python

from time import sleep
import subprocess
import re
import sys, getopt, string

def help_message():
    print '''ubnt_signal_reader.py -- uses espeak and ssh on Linux boxes to read out loud the connection strength of a Ubiquiti AirMax device
    Useage examples:
    
        python ubnt_signal_reader.py
        Will default to Ubiquiti default host IP (192.168.1.20) and default pause between readings (2 seconds).
    
        python ubnt_signal_reader.py -s 5
        Uses Ubiquiti default host IP, but will sleep for 5 seconds.  
        
        python ubnt_signal_reader.py -s 10 10.1.1.1
        Sleeps for 10 seconds in between reading signal strengths from Ubiquiti device at 10.1.1.1.
        
        python ubnt_signal_reader.py help
        This help message.
        
Since SSH is used underneath, actual resolvable hostnames can be used instead of IP addresses.

To make the best use of this script, is it helpful to create a local SSH key with no passphrase and transfer it to the Ubiquiti device, like so:

$ ssh-keygen -t dsa (hit enter three times for no passphrase)
$ ssh-copy-id admin@hostname'''
    
    sys.exit(0)
          
# get regular expression ready
p = re.compile('=-(.* dBm)  Noise', re.IGNORECASE)

# set default values
host = '192.168.1.20'
sleep_time = 2

# try grabbing cli arguments and using instead of defaults
try:
    options, xarguments = getopt.getopt(sys.argv[1:], 's', [])
    
    if 'help' in options or 'help' in xarguments:
        help_message()
except SystemExit:
    sys.exit()
except:
    options = []

for option in options[:]:
    
    if option[0] == '-s':
        sleep_time = xarguments[0]
        options.remove(option)
        xarguments.remove(sleep_time)
        sleep_time = float(sleep_time)

try:
    host = xarguments[0]
except:
    print 'Using default Ubiquiti device IP of 192.168.1.20'

# start main loop
while 1:
    try:
        strength = subprocess.Popen(['ssh', 'admin@' + host, "'iwconfig'", '2>/dev/null'], shell=False, stdout=subprocess.PIPE)
        strength = p.search(strength.communicate()[0])
        subprocess.Popen(['espeak', strength.group(1)], shell=False, stdout=subprocess.PIPE) 
        sleep(sleep_time)
    except KeyboardInterrupt:
        sys.exit('Caught Ctrl-C, exiting')
    except AttributeError:
        sys.exit('Apparent network error, exiting.')
    except:
        sys.exit('Exiting for unknown reason.')
