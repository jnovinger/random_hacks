#!/usr/bin/env python

from time import sleep, localtime, strftime
import urllib2
import hashlib
from sys import exit, argv, exc_info

if len(argv) > 1:
    url = argv[1]
else:
    print "usage: python page-archive.py <url> [filename prefix]."
    exit(0)

if len(argv) > 2:
    file_prefix = argv[2]
else:
    file_prefix = 'archive'

last_hash = ''
secs = 10

while True:
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        new_time = localtime()

        m = hashlib.sha512()
        m.update(html)
        curr_hash = m.digest()
        if last_hash != curr_hash:
            # save a copy to play with later
            file_name = "%s-%s.html" % (file_prefix, strftime("%m%d%Y_%H%M%S", new_time))

            try:
                local_file = open(file_name, 'w')
            except IOError:
                print "%r is not a legal filename prefix." % file_prefix
                exit(1)

            local_file.write(html)
            local_file.close()


            success = ""
        else:
            success = " not"

        # drop a note
        print "<%s> has%s changed at %s. Sleeping for %s seconds." % (url, success, strftime("%a, %d %b %Y %H:%M:%S +0600", new_time), secs)


        last_hash = curr_hash
        sleep(secs)

    except SystemExit:
        # catch exit() bubbling up and pass it on
        exit(1)

    except KeyboardInterrupt:
        # user killed the process
        print "\n%s terminated." % argv[0]
        exit(0)

    except IOError:
        # unable to write to file
        print "Unable to write to %r." % file_name
        exit(1)

    except:
        # caught an unexpected error, exit loudly
        print "Unexpected error:", exc_info()[0]
        exit(1)