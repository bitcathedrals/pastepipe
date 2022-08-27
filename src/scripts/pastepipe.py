
#
# pastepipe.py written by Michael Mattie (codermattie@runbox.com)
#

# a program to read from stdin and copy it to stdout and to pastebin

import requests
import sys

for line in sys.stdin:
    print(line)

