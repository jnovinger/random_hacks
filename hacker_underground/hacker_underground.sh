#!/bin/bash
## Inspired by (stolen from) http://news.ycombinator.com/item?id=2288604
## Python versions does the same thing, but is a lot more verbose

# didn't survive puzzle as of Fri, 04 Mar 2011 12:17:31 +0600

cat puzzle.txt | tr ',' '\n' | sort -n | uniq -d
