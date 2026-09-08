#!/usr/bin/env python3
"""Fetch a Canvas (bCourses) calendar feed and print upcoming events as JSON.

Usage:
    python3 bcourses_feed_diff.py <ics_url> [--days 21]

Canvas publishes a per-user ICS feed at Calendar > Calendar Feed. It needs no
login, so a cloud routine can fetch it and compare titles and dates against the
MBA calendar. This script does the fetch and parse only; the routine does the
comparison and creates any missing calendar events.

Output: a JSON list of {"summary", "start", "end", "all_day", "url"} sorted by
start, limited to the next N days. Prints a one-line summary to stderr.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone


def unfold(text: str) -> list[str]:
    """Join RFC 5545 folded lines (continuations start with a space or tab)."""
    lines: list[str] = []
    for raw in text.splitlines():
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def parse_dt(value: str, params: str) -> tuple[datetime, bool]:
    """Return (aware datetime in UTC, all_day)."""
    if "VALUE=DATE" in params or re.fullmatch(r"\d{8}", value):
        d = datetime.strptime(value[:8], "%Y%m%d").replace(tzinfo=timezone.utc)
        return d, True
    if value.endswith("Z"):
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc), False
    # Floating or TZID-qualified time: treat as UTC for ordering; the routine
    # renders Pacific from the calendar side.
    return datetime.strptime(value[:15], "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc), False


def parse_ics(text: str) -> list[dict]:
    events: list[dict] = []
    current: dict | None = None
    for line in unfold(text):
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT" and current is not None:
            if "start" in current:
                events.append(current)
            current = None
        elif current is not None and ":" in line:
            head, value = line.split(":", 1)
            name, _, params = head.partition(";")
            if name == "SUMMARY":
                current["summary"] = value.replace("\\,", ",").replace("\\n", " ").strip()
            elif name == "DTSTART":
                dt, all_day = parse_dt(value, params)
                current["start"] = dt.isoformat()
                current["all_day"] = all_day
            elif name == "DTEND":
                current["end"] = parse_dt(value, params)[0].isoformat()
            elif name == "URL":
                current["url"] = value
    return events


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    url = argv[1]
    days = 21
    if "--days" in argv:
        days = int(argv[argv.index("--days") + 1])
    with urllib.request.urlopen(url, timeout=30) as resp:
        text = resp.read().decode("utf-8", "replace")
    now = datetime.now(timezone.utc)
    horizon = now + timedelta(days=days)
    events = [e for e in parse_ics(text) if now - timedelta(days=1) <= datetime.fromisoformat(e["start"]) <= horizon]
    events.sort(key=lambda e: e["start"])
    json.dump(events, sys.stdout, indent=1)
    print(f"\n{len(events)} events inside {days} days", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
