#!/usr/bin/python

# Copyright (C)  2025 Alexandre Borges <reverseexploit@proton.me>
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

import sys
import argparse
import requests
import json
import re
from urllib.parse import urljoin
from colorama import init, Fore, Style

__author__ = "Alexandre Borges"
__copyright__ = "Copyright 2025, Alexandre Borges"
__license__ = "GNU General Public License v3.0"
__version__ = "1.5"
__email__ = "reverseexploit@proton.me"

# Constants

ORIG_URL = 'https://api.cfptime.org'
CFP_URL = 'https://api.cfptime.org/api/cfps'
UPCOMING_URL = 'https://api.cfptime.org/api/upcoming'

# Colors
COLORS = {
    "black": Fore.BLACK,
    "yellow": Fore.YELLOW,
    "lightgreen": Fore.LIGHTGREEN_EX,
    "pink": Fore.MAGENTA,
    "lightcyan": Fore.CYAN,
    "lightred": Fore.RED,
    "lightblue": Fore.LIGHTBLUE_EX,
    "lightmagenta": Fore.LIGHTMAGENTA_EX,
    "lightyellow": Fore.LIGHTYELLOW_EX,
    "reset": Style.RESET_ALL
}


def fetch_data(url):
    session = requests.Session()

    try:
        init_response = session.get(ORIG_URL)
        init_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during initial request: {e}")
        sys.exit(1)

    match = re.search(r'request\.headers\["X-CSRFToken"\]\s*=\s*"([^"]+)"', init_response.text)
    if not match:
        print("CSRF token not found in Swagger UI.")
        sys.exit(1)

    csrf_token = match.group(1)

    headers = {
      'Accept': 'application/json',
      'X-CSRFToken': csrf_token,
      'Referer': 'https://api.cfptime.org'
      }

    try:
    
        full_url = urljoin(url + '/', '?format=json')
        response = session.get(full_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)


def display_data(data, fields, headers):
    """Display data in a formatted table with tabs between columns."""
    print(COLORS["reset"] + "\n" + headers)
    print(COLORS["reset"] + "-" * 140)
    for item in data:
        try:
            row = "\t".join(
                COLORS[field["color"]] + f"{item.get(field['key'], '')[:field['width']]:<{field['width']}}"
                for field in fields
            )
            print(row + COLORS["reset"])
        except KeyError:
            continue
    print(COLORS["reset"])

def save_csv(data, fields, csv_headers, csvFile):
    """Save data to a CSV file with proper quoting and escaping."""
    try:
        with open(csvFile, 'w') as f:
            # Write CSV headers with quotes
            quoted_headers = ",".join([f'"{header}"' for header in csv_headers])
            f.write(quoted_headers + "\n")
            
            # Write data rows
            for item in data:
                csv_fields = []
                for field in fields:
                    value = item.get(field['key'], '')[:field['width']].rstrip()
                    # Escape double quotes by doubling them
                    escaped_value = value.replace('"', '""')
                    csv_fields.append(f'"{escaped_value}"')
                row = ",".join(csv_fields)
                f.write(row + "\n")
    except Exception as e:
        print(f"Error saving data to CSV file: {e}")
        sys.exit(1)

def cfplist(csvFile: str = None):
    """List Call For Papers."""
    data = fetch_data(CFP_URL)
    fields = [
        {"key": "name", "color": "lightyellow", "width": 35},
        {"key": "cfp_deadline", "color": "lightgreen", "width": 12},
        {"key": "conf_start_date", "color": "lightmagenta", "width": 10},
        {"key": "city", "color": "lightcyan", "width": 16},
        {"key": "twitter", "color": "lightcyan", "width": 18},
        {"key": "website", "color": "lightgreen", "width": 38},
    ]
    headers = (
        "Conference Name".ljust(35) + "\t" +
        "CFP End".ljust(15) + "\t" +
        "Conf Start".ljust(10) + "\t" +
        "City".ljust(16) + "\t" +
        "Twitter".ljust(18) + "\t" +
        "Website".ljust(38)
    )
    display_data(data, fields, headers)

    # Save the data to a CSV file if a file name is provided
    if csvFile is not None:
        csv_headers = ["Conference Name", "CFP End", "Conf Start", "City", "Twitter", "Website"]
        save_csv(data, fields, csv_headers, csvFile)

def uplist(csvFile: str = None):
    """List Upcoming Conferences."""
    data = fetch_data(UPCOMING_URL)
    fields = [
        {"key": "name", "color": "lightyellow", "width": 50},
        {"key": "city", "color": "lightcyan", "width": 20},
        {"key": "country", "color": "lightgreen", "width": 7},
        {"key": "conf_start_date", "color": "lightmagenta", "width": 10},
    ]
    headers = (
        "Conference Name".ljust(50) + "\t" +
        "City".ljust(20) + "\t" +
        "Country".ljust(7) + "\t" +
        "Conference Date".ljust(10)
    )
    display_data(data, fields, headers)

    # Save the data to a CSV file if a file name is provided
    if csvFile is not None:
        csv_headers = ["Conference Name", "City", "Country", "Conference Date"]
        save_csv(data, fields, csv_headers, csvFile)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="CFPsec lists Call For Papers or upcoming Hacking/Security Conferences based on cfptime.org website.",
        usage="python cfpsec.py [--cfp] [--up] [-csv <filename>]"
    )
    parser.add_argument('--cfp', action='store_true', help='List Call For Papers of Hacking/Security Conferences.')
    parser.add_argument('--up', action='store_true', help='List all upcoming Hacking/Security Conferences.')
    parser.add_argument('-csv', type=str, default="", required=False, help="Name of the CSV file to save the data.")

    args = parser.parse_args()
    csvFile = args.csv if "csv" in args else None

    if args.cfp:
        cfplist(csvFile)
    elif args.up:
        uplist(csvFile)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
