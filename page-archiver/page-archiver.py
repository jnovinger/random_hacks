#!/usr/bin/env python

from time import sleep, localtime, strftime
import urllib2
import hashlib
from sys import exit, argv

if len(argv) > 1:
    url = argv[1]
else:
    print "usage: python page-archive.py <url>."
    exit(0)

last_hash = ''
secs = 10

while True:
    try:
        response = urllib2.urlopen(url)
        html = response.read()

        m = hashlib.sha512()
        m.update(html)
        curr_hash = m.digest()
        if last_hash != curr_hash:
            # save a copy to play with later
            file_name = "smartbear-%s.html" % strftime("%m%d%Y_%H%M%S", localtime())
            local_file = open(file_name, 'w')
            local_file.write(html)
            local_file.close()

            success = ""
        else:
            success = " not"
            
        # drop a note
        print "<%s> has%s changed at %s. Sleeping for %s seconds." % (url, success, strftime("%a, %d %b %Y %H:%M:%S +0600", localtime()), secs)
        last_hash = curr_hash

        sleep(secs)

    except KeyboardInterrupt:
        print "\npage-archiver terminated\n"
        exit(0)

    except:
        pass