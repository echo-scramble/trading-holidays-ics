#!/usr/bin/env python3

import re
from datetime import datetime

# Read file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Find the position to insert new events (after the last VTIMEZONE and before first VEVENT)
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')

# Split content
header = content[:header_end]
events_section = content[header_end:footer_start]
footer = content[footer_start:]

# Parse existing events
existing_events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', events_section, re.DOTALL)

# Fix 1: Update 2025 Jan 1 to include German market
for i, event in enumerate(existing_events):
    if '20250101' in event and 'New Year\'s Day' in event:
        # Update summary to include German
        event = event.replace(
            'SUMMARY:🇬🇧🇺🇸 New Year\'s Day - Closed',
            'SUMMARY:🇩🇪🇬🇧🇺🇸 Neujahr / New Year\'s Day - Closed'
        )
        # Update description
        event = event.replace(
            'DESCRIPTION:ICE Futures Europe (Brent) and US commodity futures markets closed all day',
            'DESCRIPTION:German stock markets, ICE Futures Europe (Brent) and US commodity futures markets closed all day'
        )
        # Update categories
        event = event.replace(
            'CATEGORIES:UK,US,Full Day',
            'CATEGORIES:DE,UK,US,Full Day'
        )
        # Update UID
        event = event.replace(
            'UID:20250101-us-closed@trading-holidays.com',
            'UID:20250101-de-uk-us-closed@trading-holidays.com'
        )
        existing_events[i] = event
        break

# Create missing events
new_events = []

# 2027 Dec 25 - 1. Weihnachtstag
event_20271225 = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:20271225
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20271225-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪 1. Weihnachtstag - Closed
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
new_events.append(event_20271225)

# 2027 Dec 26 - 2. Weihnachtstag
event_20271226 = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:20271226
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20271226-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪 2. Weihnachtstag - Closed
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
new_events.append(event_20271226)

# 2028 Jan 1 - Neujahr
event_20280101 = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:20280101
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20280101-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪 Neujahr - Closed
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
new_events.append(event_20280101)

# 2028 Dec 24 - Heiligabend
event_20281224 = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:20281224
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20281224-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪 Heiligabend (Christmas Eve) - Closed
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
new_events.append(event_20281224)

# Also add US early close for Dec 24, 2028
event_20281224_us = f"""BEGIN:VEVENT
DTSTART;TZID=America/New_York:20281224T093000
DTEND;TZID=America/New_York:20281224T130000
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20281224-us-early@trading-holidays.com
SEQUENCE:1
SUMMARY:🇺🇸 Christmas Eve - Early Close
DESCRIPTION:US commodity futures markets close at 12:00 PM CT / 1:00 PM ET
CATEGORIES:US,Early Close
TRANSP:TRANSPARENT
END:VEVENT"""
new_events.append(event_20281224_us)

# Combine all events and sort by date
all_events = existing_events + new_events

def extract_date(event_text):
    # Try DATETIME first
    match = re.search(r'DTSTART;[^:]+:(\d{8})', event_text)
    if match:
        return match.group(1)
    # Then DATE
    match = re.search(r'DTSTART;VALUE=DATE:(\d{8})', event_text)
    if match:
        return match.group(1)
    return '99999999'

all_events.sort(key=extract_date)

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(all_events))
    f.write(footer)

print(f"Added missing German holidays. Total events now: {len(all_events)}")