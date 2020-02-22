# cfpsec
CFPsec is program to list Call For Papers or upcoming Hacking/Security Conferences based on cfptime.org website.

[<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/alexandreborges/cfpsec?color=Red&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases/tag/1.0) [<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/alexandreborges/cfpsec?color=Yellow&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases) [<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/alexandreborges/cfpsec?label=Release%20Date&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases) [<img alt="GitHub" src="https://img.shields.io/github/license/alexandreborges/cfpsec?style=for-the-badge">](https://github.com/alexandreborges/cfpsec/blob/master/LICENSE) 
[<img alt="GitHub stars" src="https://img.shields.io/github/stars/alexandreborges/cfpsec?logoColor=Red&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/stargazers) [<img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/ale_sp_brazil?color=blueviolet&style=for-the-badge">](https://twitter.com/ale_sp_brazil)

![Alt text](pictures/picture_1.jpg?raw=true "Title")
![Alt text](pictures/picture_2.jpg?raw=true "Title")

Copyright (C)  2020 Alexandre Borges <alexandreborges at blackstormsecurity dot com>

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      See GNU Public License on <http://www.gnu.org/licenses/>.
      
 # Current Version: 1.0
 
 CFPsec has been tested on Ubuntu, Kali Linux 2019, Windows 8.1 and 10. Before using CFPsec, execute:

        $ pip3.7 install -r requirements.txt
 
 # USAGE

To use the CFPsec, execute the command as shown below:

      root@ubuntu19:~/github/cfpsec# python3.7 cfpsec.py -c 1 (Linux)
      root@ubuntu19:~/github/cfpsec# python3.7 cfpsec.py -u 1 (Linux)
      C:\github> python3.7 cfpsec.py -c 1 -w 1 (Windows)
      C:\github> python3.7 cfpsec.py -u 1 -w 1 (Windows)

      usage: usage: python cfpsec.py -c <0|1> -u <0|1> -w <0|1>
      
      Optional arguments:
      
      -h, --help            show this help message and exit
      -c CFP, --cfp CFP     List Call For Papers of Hacking/Securiy Conferences.
      -u UPCOMING, --upcoming UPCOMING List all upcoming Hacking/Security Conferences.
      -w WIN, --win WIN     Set to 1 whether you running on Windows.
 
 # HISTORY

Version 1.0:

      This version:
      
            * Includes the -c option to list Call for Papers of Hacking/Security Conferences. 
            * Includes the -u option to list upcoming Hacking/Security Conferences.
