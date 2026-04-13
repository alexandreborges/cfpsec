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

import csv
import json
import os
import re
import signal
import sys
import argparse
import requests
from datetime import date, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from colorama import init, Fore, Style

__author__ = "Alexandre Borges"
__copyright__ = "Copyright 2025, Alexandre Borges"
__license__ = "GNU General Public License v3.0"
__version__ = "2.0.2"
__email__ = "reverseexploit@proton.me"

init(autoreset=False)

CFP_URL         = "https://api.cfptime.org/api/cfps/"
CFP_DETAIL_URL  = "https://api.cfptime.org/api/cfps/{id}/"
CONF_URL        = "https://api.cfptime.org/api/conferences/"
CONF_DETAIL_URL = "https://api.cfptime.org/api/conferences/{id}/"
UPCOMING_URL    = "https://api.cfptime.org/api/upcoming/"
PREVIOUS_URL    = "https://api.cfptime.org/api/previously/"

_PALETTE_DARK = {
    "conf_name":   Fore.LIGHTYELLOW_EX,
    "date":        Fore.LIGHTGREEN_EX,
    "conf_date":   Fore.LIGHTMAGENTA_EX,
    "location":    Fore.CYAN,
    "misc":        Fore.LIGHTBLUE_EX,
    "error":       Fore.RED,
    "banner_logo": Fore.LIGHTCYAN_EX,
    "banner_text": Fore.LIGHTYELLOW_EX,
    "reset":       Style.RESET_ALL,
}
_PALETTE_LIGHT = {
    "conf_name":   Fore.YELLOW,
    "date":        Fore.GREEN,
    "conf_date":   Fore.MAGENTA,
    "location":    Fore.BLUE,
    "misc":        Fore.CYAN,
    "error":       Fore.RED,
    "banner_logo": Fore.BLUE,
    "banner_text": Fore.MAGENTA,
    "reset":       Style.RESET_ALL,
}

_SEMANTIC = {
    "lightyellow":  "conf_name",
    "lightgreen":   "date",
    "lightmagenta": "conf_date",
    "lightcyan":    "location",
    "lightblue":    "misc",
    "lightred":     "error",
}


def _detect_dark_background():
    """Return True when the terminal background is dark (the common case).

    Reads COLORFGBG exported by xterm, rxvt, iTerm2, etc.
    Format is 'fg;bg'; bg < 8 means dark. Falls back to True when absent.
    """
    colorfgbg = os.environ.get("COLORFGBG", "")
    if colorfgbg:
        try:
            bg = int(colorfgbg.split(";")[-1])
            return bg < 8
        except ValueError:
            pass
    return True


def _build_colors(dark):
    """Return a COLORS dict resolved against the correct palette."""
    palette = _PALETTE_DARK if dark else _PALETTE_LIGHT
    colors = {"reset": Style.RESET_ALL}
    for semantic_key, palette_key in _SEMANTIC.items():
        colors[semantic_key] = palette[palette_key]
    colors["banner_logo"] = palette["banner_logo"]
    colors["banner_text"] = palette["banner_text"]
    colors["error"]       = palette["error"]
    return colors


COLORS: dict = {"reset": Style.RESET_ALL}


def _sigint_handler(_signum, _frame):
    """Reset terminal colours and exit cleanly on Ctrl+C."""
    print(COLORS["reset"])
    sys.exit(0)


signal.signal(signal.SIGINT, _sigint_handler)
signal.signal(signal.SIGTERM, _sigint_handler)


def print_banner():
    """Print the tool banner."""
    banner = f"""
{COLORS["banner_logo"]}  ██████╗███████╗██████╗ ███████╗███████╗ ██████╗
{COLORS["banner_logo"]} ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝
{COLORS["banner_logo"]} ██║     █████╗  ██████╔╝███████╗█████╗  ██║
{COLORS["banner_logo"]} ██║     ██╔══╝  ██╔═══╝ ╚════██║██╔══╝  ██║
{COLORS["banner_logo"]} ╚██████╗██║     ██║     ███████║███████╗╚██████╗
{COLORS["banner_logo"]}  ╚═════╝╚═╝     ╚═╝     ╚══════╝╚══════╝ ╚═════╝
{COLORS["banner_text"]}
  CFPsec v{__version__} | Author: {__author__}
  Security/Hacking Conference CFPs & Upcoming Events
  Data source: cfptime.org
{COLORS["reset"]}"""
    print(banner)


def _create_session():
    """Create an HTTP session with automatic retry on transient errors."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


_ANSI_ESCAPE_RE = re.compile(
    r'\x1b(?:'
    r'\][^\x07\x1b]*(?:\x07|\x1b\\)'
    r'|[@-Z\\-_]'
    r'|\[[0-?]*[ -/]*[@-~]'
    r')'
    r'|[\x80-\x9f]'
)
_CSV_FORMULA_CHARS = ('=', '+', '-', '@', '\t', '\r')


def _strip_ansi(text):
    """Remove ANSI escape sequences from API data to prevent terminal injection."""
    return _ANSI_ESCAPE_RE.sub('', text)


def _sanitize_csv_cell(value):
    """Prefix formula-trigger characters to prevent CSV injection in spreadsheets."""
    s = str(value)
    if s.startswith(_CSV_FORMULA_CHARS):
        return "'" + s
    return s


def fetch_data(url, params=None):
    """Fetch JSON from *url*, passing optional query *params*.

    Returns the parsed JSON value (list or dict).
    """
    try:
        session = _create_session()
        session.headers.update({
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        })
        response = session.get(url, params=params, timeout=15, verify=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(COLORS["error"] + f"Error fetching data: {e}" + COLORS["reset"])
        sys.exit(1)

    try:
        return response.json()
    except ValueError as e:
        snippet = _strip_ansi(response.text[:300].strip()) if response.text else "<empty body>"
        print(COLORS["error"] + f"Error parsing API response (HTTP {response.status_code}): {e}" + COLORS["reset"])
        print(COLORS["error"] + f"Response body: {snippet}" + COLORS["reset"])
        sys.exit(1)


def _apply_filters(data, keyword=None, country=None):
    """Filter a list by keyword (name/city) and/or country."""
    if keyword:
        kw = keyword.lower()
        data = [
            item for item in data
            if kw in item.get("name", "").lower()
            or kw in item.get("city", "").lower()
        ]
    if country:
        cc = country.lower()
        data = [
            item for item in data
            if cc in item.get("country", "").lower()
        ]
    return data


def _filter_future(data, date_key):
    """Keep only items whose *date_key* is today or in the future."""
    today = date.today()
    result = []
    for item in data:
        raw = item.get(date_key, "")
        if not raw:
            continue
        try:
            if date.fromisoformat(str(raw)[:10]) >= today:
                result.append(item)
        except ValueError:
            continue
    return result


def _filter_by_days(data, date_key, days):
    """Keep only items whose *date_key* falls within the next *days* days."""
    today = date.today()
    cutoff = today + timedelta(days=days)
    result = []
    for item in data:
        raw = item.get(date_key, "")
        if not raw:
            continue
        try:
            d = date.fromisoformat(str(raw)[:10])
            if today <= d <= cutoff:
                result.append(item)
        except ValueError:
            continue
    return result


def _sort_by_date(data, date_key):
    """Sort by an ISO date field, placing missing/empty dates last."""
    return sorted(data, key=lambda item: item.get(date_key) or "9999-99-99")


def _apply_limit(data, limit):
    """Truncate list to *limit* items when limit is set."""
    if limit and limit > 0:
        return data[:limit]
    return data


def display_text(data, fields, headers):
    """Render data as a colour-formatted table."""
    print(COLORS["reset"] + "\n" + headers)
    print(COLORS["reset"] + "-" * 140)
    for item in data:
        try:
            row = "\t".join(
                COLORS[field["color"]]
                + f"{_strip_ansi(str(item.get(field['key'], '')))[:field['width']]:<{field['width']}}"
                for field in fields
            )
            print(row + COLORS["reset"])
        except KeyError:
            continue
    print(COLORS["reset"])


def display_json(data, fields):
    """Render data as JSON (field-filtered)."""
    keys = [f["key"] for f in fields]
    output = [{k: item.get(k, "") for k in keys} for item in data]
    print(json.dumps(output, indent=2, ensure_ascii=False))


def display_csv(data, fields):
    """Render data as CSV (field-filtered, formula-safe)."""
    keys = [f["key"] for f in fields]
    writer = csv.DictWriter(sys.stdout, fieldnames=keys, extrasaction="ignore",
                            lineterminator="\n")
    writer.writeheader()
    for item in data:
        writer.writerow({k: _sanitize_csv_cell(item.get(k, "")) for k in keys})


def display_data(data, fields, headers, output_format="text"):
    """Dispatch to the appropriate output formatter."""
    if output_format == "json":
        display_json(data, fields)
    elif output_format == "csv":
        display_csv(data, fields)
    else:
        display_text(data, fields, headers)


def display_detail(item, label_fields, output_format="text"):
    """Render a single conference or CFP record.

    *label_fields* is a list of dicts with keys: label, key, color.
    """
    if output_format == "json":
        print(json.dumps(item, indent=2, ensure_ascii=False))
        return
    if output_format == "csv":
        keys = [f["key"] for f in label_fields]
        writer = csv.DictWriter(sys.stdout, fieldnames=keys, extrasaction="ignore",
                                lineterminator="\n")
        writer.writeheader()
        writer.writerow({k: _sanitize_csv_cell(item.get(k, "")) for k in keys})
        return
    print(COLORS["reset"] + "\n" + "-" * 80)
    for field in label_fields:
        val = _strip_ansi(str(item.get(field["key"]) or "")).strip()
        if val:
            label = COLORS["lightcyan"] + field["label"].ljust(22) + COLORS["reset"]
            value = COLORS[field["color"]] + val + COLORS["reset"]
            print(f"  {label}: {value}")
    print(COLORS["reset"] + "-" * 80 + "\n")


_FIELDS_CONFERENCE = [
    {"key": "name",            "color": "lightyellow",  "width": 45},
    {"key": "conf_start_date", "color": "lightmagenta", "width": 12},
    {"key": "city",            "color": "lightcyan",    "width": 18},
    {"key": "country",         "color": "lightgreen",   "width": 7},
    {"key": "website",         "color": "lightgreen",   "width": 38},
]
_HEADERS_CONFERENCE = (
    "Conference Name".ljust(45) + "\t"
    + "Start Date".ljust(12) + "\t"
    + "City".ljust(18) + "\t"
    + "Country".ljust(7) + "\t"
    + "Website".ljust(38)
)

_DETAIL_FIELDS = [
    {"label": "Name",             "key": "name",             "color": "lightyellow"},
    {"label": "CFP Deadline",     "key": "cfp_deadline",     "color": "lightgreen"},
    {"label": "Conference Start", "key": "conf_start_date",  "color": "lightmagenta"},
    {"label": "City",             "key": "city",             "color": "lightcyan"},
    {"label": "Province",         "key": "province",         "color": "lightcyan"},
    {"label": "Country",          "key": "country",          "color": "lightcyan"},
    {"label": "Twitter",          "key": "twitter",          "color": "lightblue"},
    {"label": "Website",          "key": "website",          "color": "lightgreen"},
    {"label": "CFP Details",      "key": "cfp_details",      "color": "lightyellow"},
    {"label": "Speaker Benefits", "key": "speaker_benefits", "color": "lightgreen"},
    {"label": "Code of Conduct",  "key": "code_of_conduct",  "color": "lightblue"},
    {"label": "Number of Days",   "key": "number_of_days",   "color": "lightmagenta"},
]


def cfplist(keyword=None, sort=False, limit=None, days=None, output_format="text"):
    """List open Call For Papers."""
    data = fetch_data(CFP_URL)
    data = _apply_filters(data, keyword=keyword)
    if days:
        data = _filter_by_days(data, "cfp_deadline", days)
    if sort:
        data = _sort_by_date(data, "cfp_deadline")
    data = _apply_limit(data, limit)

    fields = [
        {"key": "name",            "color": "lightyellow",  "width": 35},
        {"key": "cfp_deadline",    "color": "lightgreen",   "width": 12},
        {"key": "conf_start_date", "color": "lightmagenta", "width": 10},
        {"key": "city",            "color": "lightcyan",    "width": 16},
        {"key": "twitter",         "color": "lightcyan",    "width": 18},
        {"key": "website",         "color": "lightgreen",   "width": 38},
    ]
    headers = (
        "Conference Name".ljust(35) + "\t"
        + "CFP End".ljust(12) + "\t"
        + "Conf Start".ljust(10) + "\t"
        + "City".ljust(16) + "\t"
        + "Twitter".ljust(18) + "\t"
        + "Website".ljust(38)
    )
    display_data(data, fields, headers, output_format)


def uplist(keyword=None, country=None, sort=False, limit=None, days=None,
           output_format="text"):
    """List upcoming conferences."""
    data = fetch_data(UPCOMING_URL)
    data = _apply_filters(data, keyword=keyword, country=country)
    if days:
        data = _filter_by_days(data, "conf_start_date", days)
    if sort:
        data = _sort_by_date(data, "conf_start_date")
    data = _apply_limit(data, limit)

    fields = [
        {"key": "name",            "color": "lightyellow",  "width": 50},
        {"key": "city",            "color": "lightcyan",    "width": 20},
        {"key": "country",         "color": "lightgreen",   "width": 7},
        {"key": "conf_start_date", "color": "lightmagenta", "width": 10},
    ]
    headers = (
        "Conference Name".ljust(50) + "\t"
        + "City".ljust(20) + "\t"
        + "Country".ljust(7) + "\t"
        + "Conference Date".ljust(10)
    )
    display_data(data, fields, headers, output_format)


def conflist(keyword=None, country=None, sort=False, limit=None, days=None,
             output_format="text"):
    """List all conferences (open CFP + upcoming combined)."""
    data = fetch_data(CONF_URL)
    data = _filter_future(data, "conf_start_date")
    data = _apply_filters(data, keyword=keyword, country=country)
    if days:
        data = _filter_by_days(data, "conf_start_date", days)
    if sort:
        data = _sort_by_date(data, "conf_start_date")
    data = _apply_limit(data, limit)
    display_data(data, _FIELDS_CONFERENCE, _HEADERS_CONFERENCE, output_format)


def prevlist(keyword=None, country=None, sort=False, limit=None, days=None,
             page=None, page_size=None, output_format="text"):
    """List previously held conferences (server-side paginated)."""
    params = {}
    if page:
        params["page"] = page
    if page_size:
        params["page_size"] = page_size

    raw = fetch_data(PREVIOUS_URL, params=params or None)

    if isinstance(raw, dict) and "results" in raw:
        data = raw["results"]
        try:
            total = int(raw.get("count", len(data)))
        except (ValueError, TypeError):
            total = len(data)
        if output_format == "text":
            page_info = f"  Page {page or 1} — showing {len(data)} of {total} records"
            print(COLORS["lightblue"] + page_info + COLORS["reset"])
    else:
        data = raw

    data = _apply_filters(data, keyword=keyword, country=country)
    if days:
        data = _filter_by_days(data, "conf_start_date", days)
    if sort:
        data = _sort_by_date(data, "conf_start_date")
    data = _apply_limit(data, limit)
    display_data(data, _FIELDS_CONFERENCE, _HEADERS_CONFERENCE, output_format)


def cfp_detail(cfp_id, output_format="text"):
    """Show full detail for a single CFP by ID."""
    url = CFP_DETAIL_URL.format(id=cfp_id)
    item = fetch_data(url)
    display_detail(item, _DETAIL_FIELDS, output_format)


def conf_detail(conf_id, output_format="text"):
    """Show full detail for a single conference by ID."""
    url = CONF_DETAIL_URL.format(id=conf_id)
    item = fetch_data(url)
    display_detail(item, _DETAIL_FIELDS, output_format)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description=(
            "CFPsec lists Call For Papers and Hacking/Security Conferences "
            "from cfptime.org."
        ),
        usage="cfpsec <action> [options]",
    )

    action_group = parser.add_argument_group("Actions")
    action_group.add_argument(
        "--cfp", action="store_true",
        help="List open Call For Papers.")
    action_group.add_argument(
        "--up", action="store_true",
        help="List upcoming conferences.")
    action_group.add_argument(
        "--conf", action="store_true",
        help="List all conferences (open CFP + upcoming combined).")
    action_group.add_argument(
        "--prev", action="store_true",
        help="List previously held conferences (paginated).")
    action_group.add_argument(
        "--cfp-id", metavar="ID", dest="cfp_id", type=int,
        help="Show full detail for a single CFP by its numeric ID.")
    action_group.add_argument(
        "--conf-id", metavar="ID", dest="conf_id", type=int,
        help="Show full detail for a single conference by its numeric ID.")

    filter_group = parser.add_argument_group("Filtering & Sorting")
    filter_group.add_argument(
        "--filter", metavar="KEYWORD",
        help="Filter by conference name or city (case-insensitive).")
    filter_group.add_argument(
        "--country", metavar="CC",
        help="Filter by country name or code.")
    filter_group.add_argument(
        "--days", metavar="N", type=int,
        help="Show only events starting within the next N days.")
    filter_group.add_argument(
        "--sort", action="store_true",
        help="Sort by date (CFP deadline for --cfp, start date otherwise).")
    filter_group.add_argument(
        "--limit", metavar="N", type=int,
        help="Cap the number of rows displayed.")

    page_group = parser.add_argument_group("Pagination (--prev only)")
    page_group.add_argument(
        "--page", metavar="N", type=int,
        help="Page number for --prev results.")
    page_group.add_argument(
        "--page-size", metavar="N", type=int, dest="page_size",
        help="Number of records per page for --prev results.")

    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "--output", choices=["text", "json", "csv"], default="text",
        metavar="FORMAT",
        help="Output format: text (default), json, or csv.")
    output_group.add_argument(
        "--background", choices=["dark", "light"], default=None,
        metavar="BG",
        help="Terminal background: dark or light (default: auto-detected).")
    output_group.add_argument(
        "-q", "--quiet", action="store_true",
        help="Suppress the banner.")
    output_group.add_argument(
        "--version", action="version", version=f"cfpsec {__version__}")

    args = parser.parse_args()

    if args.background is not None:
        dark = args.background == "dark"
    else:
        dark = _detect_dark_background()
    COLORS.update(_build_colors(dark))

    if not args.quiet and args.output == "text":
        print_banner()

    if args.cfp:
        cfplist(keyword=args.filter, sort=args.sort, limit=args.limit,
                days=args.days, output_format=args.output)
    elif args.up:
        uplist(keyword=args.filter, country=args.country, sort=args.sort,
               limit=args.limit, days=args.days, output_format=args.output)
    elif args.conf:
        conflist(keyword=args.filter, country=args.country, sort=args.sort,
                 limit=args.limit, days=args.days, output_format=args.output)
    elif args.prev:
        prevlist(keyword=args.filter, country=args.country, sort=args.sort,
                 limit=args.limit, days=args.days, page=args.page,
                 page_size=args.page_size, output_format=args.output)
    elif args.cfp_id:
        cfp_detail(args.cfp_id, output_format=args.output)
    elif args.conf_id:
        conf_detail(args.conf_id, output_format=args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
