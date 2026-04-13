# cfpsec
CFPsec is program to list Call For Papers or upcoming Hacking/Security Conferences based on cfptime.org website.

[<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/alexandreborges/cfpsec?color=Red&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases/tag/2.0) [<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/alexandreborges/cfpsec?color=Yellow&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases) [<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/alexandreborges/cfpsec?label=Release%20Date&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/releases) [<img alt="GitHub" src="https://img.shields.io/github/license/alexandreborges/cfpsec?style=for-the-badge">](https://github.com/alexandreborges/cfpsec/blob/master/LICENSE) 
[<img alt="GitHub stars" src="https://img.shields.io/github/stars/alexandreborges/cfpsec?logoColor=Red&style=for-the-badge">](https://github.com/alexandreborges/cfpsec/stargazers) [<img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/ale_sp_brazil?color=blueviolet&style=for-the-badge">](https://twitter.com/ale_sp_brazil)

![Alt text](pictures/picture_1.jpg?raw=true "Title")
![Alt text](pictures/picture_2.jpg?raw=true "Title")

### Copyright (C)  2026 Alexandre Borges

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      See GNU Public License on <http://www.gnu.org/licenses/>.
      
### Current Version: 2.0
 
CFPsec has been tested on Ubuntu and Windows 11. Likely, it also works on other 
operating systems. Before using CFPsec, execute:

        $ Install Python 3.9 or newer.
        $ pip install cfpsec
 
### USAGE

To use the CFPsec, execute the command as shown below:

      usage: cfpsec <action> [options]

      Actions:
        --cfp               List open Call For Papers.
        --up                List upcoming conferences.
        --conf              List all conferences (open CFP + upcoming combined).
        --prev              List previously held conferences (paginated).
        --cfp-id ID         Show full detail for a single CFP by its numeric ID.
        --conf-id ID        Show full detail for a single conference by its numeric ID.

      Filtering & Sorting:
        --filter KEYWORD    Filter by conference name or city (case-insensitive).
        --country CC        Filter by country name or code.
        --days N            Show only events starting within the next N days.
        --sort              Sort by date.
        --limit N           Cap the number of rows displayed.

      Pagination (--prev only):
        --page N            Page number.
        --page-size N       Number of records per page.

      Output:
        --output FORMAT     Output format: text (default), json, or csv.
        --background BG     Terminal background: dark or light (default: auto-detected).
        -q, --quiet         Suppress the banner.
        --version           Show program version and exit.
        -h, --help          Show this help message and exit.
 
### HISTORY


Version 2.0:

      This version:

            * Adds --conf option to list all conferences (open CFP + upcoming combined).
            * Adds --prev option to list previously held conferences with server-side pagination (--page, --page-size).
            * Adds --cfp-id and --conf-id options for full detail view of a single record.
            * Adds --filter keyword search by conference name or city.
            * Adds --country filter for country-based filtering.
            * Adds --days filter to show only events within the next N days.
            * Adds --sort to order results by date.
            * Adds --limit to cap the number of displayed rows.
            * Adds --output json|csv for structured output suitable for scripting.
            * Adds --background dark|light with automatic terminal background detection (COLORFGBG).
            * Adds -q/--quiet flag to suppress the banner.
            * Adds --version flag.
            * Adds startup banner with tool name, version, and author.
            * Fixes colorama initialization for correct ANSI support on Windows.
            * Adds HTTP retry logic with exponential backoff on transient server errors.
            * Adds browser-compatible User-Agent header required by the cfptime.org API.
            * Adds ANSI escape sequence sanitization to prevent terminal injection from API data.
            * Adds CSV formula injection protection for spreadsheet safety.
            * Fixes unhandled JSONDecodeError with improved API error diagnostics.
            * Enforces integer type on --cfp-id and --conf-id to prevent URL injection.
            * Removes simplejson dependency (standard library json is used throughout).
            * Updates minimum dependency versions: colorama>=0.4.6, requests>=2.26.0.

Version 1.5:

      This version:

            * Fixes the --cfp option to reflect a structural change on the cfptime.org.

Version 1.4:

      This version:
      
            * Presents a full refactoring of the code. 

Version 1.3:

      This version:
      
            * Fixes have been introduced. 
            * Slight changes in the Python code. 

Version 1.2:

      This version:
      
            * Small fixes have been introduced. 
            * Small structure change. 

Version 1.0.2:

      This version:
      
            * Introduces a small fix. 

Version 1.0.1:

      This version:
      
            * Introduces the possibility to install the cfpsec by using 
            the Python pip module: pip install cfpsec. 

Version 1.0:

      This version:
      
            * Includes the -c option to list Call for Papers of Hacking/Security Conferences. 
            * Includes the -u option to list upcoming Hacking/Security Conferences.
