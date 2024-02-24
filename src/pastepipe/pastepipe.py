#! /usr/bin/env python3

#
# pastepipe.py written by Michael Mattie (codermattie@runbox.com)
#

# a program to read from stdin and copy it to stdout and to pastebin

import requests
import sys
import os
import argparse
from copy import deepcopy

from pprint import pprint

ENDPOINT='https://pastebin.com/api/api_post.php'

VISIBILITY = {
	'public': 0,
	'unlisted': 1,
	'private': 2
}

EXPIRE='1d'
OPTION='paste'

PASTE_FORMAT='php'

def exec():
    parser = argparse.ArgumentParser("copy stdin to stdout and pastebin")

    parser.add_argument("name", 
                        help="name of the paste (required)")
    parser.add_argument("--visibility", 
                        help="visiblity = public|unlisted|private", 
                        required=False, default='public')
    parser.add_argument("--key", 
                        help="defaults to a file containing the API key, just the key one line of not specified",
                        required=False)

    parser.add_argument("-v",
                        dest='verbose', 
                        help="verbose, print payload without content",
                        required=False, default=False, action='store_true')

    args = parser.parse_args()

    visibility = args.visibility

    if args.visibility in VISIBILITY.keys():
        visibility = VISIBILITY[args.visibility]
    else:
        raise Exception("Unkown visibility arg: " + args.visibility)

    if args.key:
        key = args.key
    else:
        key = open(os.getenv('HOME') + "/.pastebin", "r").readline().strip()

    name = args.name 

    buffer = []

    for line in sys.stdin:
        buffer.append(line)

        print(line)
   
    payload = {
   		'api_dev_key': key,
   		'api_paste_code': "".join(buffer),
   		'api_paste_private': visibility,
   		'api_paste_name': name,
        'api_option': 'paste'
   	}

    if args.verbose:
        dump = deepcopy(payload)
    
        dump['api_paste_code'] = str(len(buffer)) + " lines of paste."

        print(">>>payload<<<<")
        pprint(dump)

    response = requests.post(ENDPOINT, payload)

    if response.status_code != 200:
        raise Exception("Got a non 200 code from pastebin: (%s): %s " % 
            (str(response.status_code),
             response.text))
    
    print("Response OK: " + response.text)

if __name__ == "__main__":
	exec()
