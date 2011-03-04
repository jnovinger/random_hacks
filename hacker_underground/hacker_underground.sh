#!/bin/bash
## Inspired by (stolen from) http://news.ycombinator.com/item?id=2288604
## Python versions does the same thing, but is a lot more verbose
cat puzzle.txt | tr ',' '\n' | sort -n | uniq -d
