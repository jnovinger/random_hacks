#!/usr/bin/env python

"""
http://kcurstream.umkc.edu:8002/listen.pls

http://www.mplayerhq.hu/DOCS/tech/slave.txt
http://code.activestate.com/recipes/542195-access-mplayer-slave-mode-from-python/
"""

from pymplayer import MPlayer
from time import sleep

if __name__ == '__main__':
    MPlayer.populate()
    try:
        url = 'http://kcurstream.umkc.edu:8002/listen.pls'

        mp = MPlayer()
        mp.loadfile(url)
        mp.command('mute')
        mp.command('volume +1')

        base_timeout = 5
        volume = 1

        while True:
            timeout = base_timeout * volume
            if volume < 14:
                mp.command('volume +1')
                volume += 1
            print volume, timeout
            sleep(timeout)
    finally:
        mp.command('quit 0')
        quit()
