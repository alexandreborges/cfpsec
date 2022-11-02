#!/usr/bin/python

# Copyright (C)  2022 Alexandre Borges <ab@blackstormsecurity.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See GNU Public License on <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import requests
import json
import time
from colorama import init, Fore, Back, Style
from datetime import datetime

__author__ = "Alexandre Borges"
__copyright__ = "Copyright 2022, Alexandre Borges"
__license__ = "GNU General Public License v3.0"
__version__ = "1.2"
__email__ = "alexandreborges at blackstormsecurity.com"

cfpurl = 'https://api.cfptime.org/api/cfps'
upurl = 'https://api.cfptime.org/api/upcoming'

class mycolors:

    reset='\033[0m'
    reverse='\033[07m'
    bold='\033[01m'
    class foreground:
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        lightgreen='\033[92m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
        red='\033[31m'
        green='\033[32m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        yellow='\033[93m'
    class background:
        black='\033[40m'
        blue='\033[44m'
        cyan='\033[46m'
        lightgrey='\033[47m'
        purple='\033[45m'
        green='\033[42m'
        orange='\033[43m'
        red='\033[41m'

def cfplist(param):

    cfptext = ''
    response = ''

    try:

        response = requests.get(param)
        cfptext = json.loads(response.text)

        if (len(cfptext) > 0):
           try:
                for i in range(0, len(cfptext)):
                   if (cfptext[i].get('name')):
                       print((mycolors.foreground.yellow + "%-35s" % cfptext[i]['name'][:35]),end='')
                       print((mycolors.foreground.lightgreen + " %s" % cfptext[i]['cfp_deadline'][:10]),end='')
                       print((mycolors.foreground.pink + " %s" % cfptext[i]['conf_start_date'][:10]),end='')
                       print((mycolors.foreground.orange + " %-16s" % cfptext[i]['city'][:16]),end='')
                       print((mycolors.foreground.lightcyan + " %-20s" % cfptext[i]['twitter'][:18]),end='')
                       print((mycolors.foreground.lightred + "%s" % cfptext[i]['website']) + mycolors.reset)
                       print(mycolors.reset, end="")
           except KeyError as e:
                pass
        print(mycolors.reset)
        exit(0)
    
    except (BrokenPipeError, IOError):
        print(mycolors.reset, file=sys.stderr)
        exit(1)

    except ValueError as e:

        print((mycolors.foreground.lightred + "Error while connecting to CFPTIME.ORG!\n"))
        print(mycolors.reset)
        exit(1)


def uplist(param):

    uptext = ''
    response = ''

    try:

        response = requests.get(param)
        uptext = json.loads(response.text)

        if (len(uptext) > 0):
           try:
                for i in range(0, len(uptext)):
                   if (uptext[i].get('name')):
                       print((mycolors.foreground.yellow + "%-50s" % uptext[i]['name'][:50]),end='')
                       print((mycolors.foreground.lightcyan + " %-20s" % uptext[i]['city'][:20]),end='')
                       print((mycolors.foreground.lightgreen + " %-7s" % uptext[i]['country']),end='')
                       print((mycolors.foreground.lightred + 4*" " + "%s" % uptext[i]['conf_start_date'][:10]) + mycolors.reset )
                       print(mycolors.reset, end="")
           except KeyError as e:
                pass
        print(mycolors.reset)
        exit(0)
    
    except (BrokenPipeError, IOError):
        print(mycolors.reset, file=sys.stderr)
        exit(1)

if __name__ == "__main__":

    cfp = 1
    upcoming = 0
    win = 0

    parser = argparse.ArgumentParser(prog=None, description="CFPsec lists Call For Papers or upcoming Hacking/Security Conferences based on cfptime.org website. The current version is 1.2", usage= "python cfpsec.py -c <0|1> -u <0|1> -w <0|1>")
    parser.add_argument('-c', '--cfp', dest='cfp',type=int, default=1, help='List Call For Papers of Hacking/Securiy Conferences.')
    parser.add_argument('-u', '--upcoming', dest='upcoming',type=int, default=0, help='List all upcoming Hacking/Security Conferences.')
    parser.add_argument('-w', '--win', dest='win',type=int, default=0, help='Set to 1 whether you are running it on Windows 10 or older.')
    
    args = parser.parse_args()

    cfpvalue = args.cfp
    upvalue = args.upcoming
    windows = args.win

    optval = [0,1]

    if (args.cfp) not in optval:
        parser.print_help()
        print(mycolors.reset)
        exit(0)

    if (args.upcoming) not in optval:
        parser.print_help()
        print(mycolors.reset)
        exit(0)
    
    if (args.win) not in optval:
        parser.print_help()
        print(mycolors.reset)
        exit(0)

    if(windows == 1):
        init(convert = True)

    if(upvalue == 1):
        cfpvalue = 0

    if (cfpvalue):
        print(mycolors.reset + "\n")
        print("Call for Papers -- Hacking and Security Conferences\n".center(140))
        print(mycolors.reset + "Conference Name".center(35) + "CFP end".center(12) + "CONF start".center(10) + "City".center(16) + "Twitter".center(18) + "Website".center(38), end='')
        print(mycolors.reset + "\n" + 140 * '-')
        cfplist(cfpurl)
        print(mycolors.reset)
        exit(0)

    if (upvalue):
        print(mycolors.reset + "\n")
        print("Upcoming Hacking and Security Conferences\n".center(100))
        print(mycolors.reset + "Conference Name".center(50) + "City".center(20) + "Country".center(7) + "Conference Date".center(24), end='')
        print(mycolors.reset + "\n" + 100 * '-')
        uplist(upurl)
        print(mycolors.reset)
        exit(0)


    print(mycolors.reset)
    exit(0)
