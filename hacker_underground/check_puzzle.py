#!/usr/bin/python

import urllib2
import hashlib
from time import sleep, localtime, strftime


# Script to check and see if the puzzle has changed

## CLI command: wget http://hackerunderground.com/ -O index.html &> /dev/null &&  cat index.html | md5sum

url = 'http://hackerunderground.com/'
last_hash = ''

while (1):
    response = urllib2.urlopen(url)
    html = response.read()

    m = hashlib.sha512()
    m.update(html)
    curr_hash = m.digest()
    if last_hash != curr_hash:
        # save a copy to play with later
        file_name = "index-%s.html" % strftime("%d-%b-%Y-%H:%M:%S", localtime())
        local_file = open(file_name, 'w')
        local_file.write(html)
        local_file.close()        
        
        # drop a note
        print "Puzzle has changed at %s. Sleeping for 60 seconds." % strftime("%a, %d %b %Y %H:%M:%S +0600", localtime())
        sleep(60)
    last_hash = curr_hash
