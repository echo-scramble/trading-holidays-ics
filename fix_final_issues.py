#!/usr/bin/env python3

import re
from datetime import datetime
from collections import defaultdict

# Holiday name mappings
HOLIDAY_NAMES = {
    '0120': 'Martin Luther King Jr. Day',
    '0217': 'Presidents\' Day',
    '0219': 'Presidents\' Day',
    '0215': 'Presidents\' Day',
    '0216': 'Presidents\' Day',
    '0220': 'Presidents\' Day',
    '0218': 'Presidents\' Day',
    '0530': 'Memorial Day',
    '0526': 'Memorial Day',
    '0525': 'Memorial Day',
    '0531': 'Memorial Day',
    '0529': 'Memorial Day',
    '0528': 'Memorial Day',
    '0527': 'Memorial Day',
    '0704': 'Independence Day',
    '0703': 'Independence Day',
    '0901': 'Labor Day',
    '0906': 'Labor Day',
    '0907': 'Labor Day',
    '0905': 'Labor Day',
    '0904': 'Labor Day',
    '0902': 'Labor Day',
    '0903': 'Labor Day',
    '1128': 'Thanksgiving',
    '1126': 'Thanksgiving',
    '1125': 'Thanksgiving',
    '1124': 'Thanksgiving',
    '1123': 'Thanksgiving',
    '1127': 'Thanksgiving',
    '1225': 'Christmas Day',
    '1224': 'Christmas Day',
    '1226': 'Christmas Day',
    '0101': 'New Year\'s Day',
    '0102': 'New Year\'s Day',
    '0103': 'New Year\'s Day',
    '1231': 'New Year\'s Day',
    # UK holidays
    '0505': 'Early May Bank Holiday',
    '0506': 'Early May Bank Holiday',
    '0507': 'Early May Bank Holiday',
    '0501': 'Early May Bank Holiday',
    '0826': 'Summer Bank Holiday',
    '0825': 'Summer Bank Holiday',
    '0831': 'Summer Bank Holiday',
    '0829': 'Summer Bank Holiday',
    '0828': 'Summer Bank Holiday',
    '0827': 'Summer Bank Holiday',
    '0830': 'Summer Bank Holiday',
    '1227': 'Christmas Day',
    '1228': 'Boxing Day',
}

# Read file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Extract header and footer
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')
header = content[:header_end]
footer = content[footer_start:]

# Extract all events
event_texts = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

def fix_event(event_text):
    """Fix individual event - add missing holiday names"""
    
    # Extract date
    date_match = re.search(r'DTSTART[^:]*:(\d{8})', event_text)
    if not date_match:
        return event_text
    
    date_str = date_match.group(1)
    month_day = date_str[4:]  # MMDD
    
    # Check if summary is missing holiday name
    summary_match = re.search(r'SUMMARY:(.*)', event_text)
    if not summary_match:
        return event_text
    
    summary = summary_match.group(1)
    
    # If summary has just flag + " - Closed", add holiday name
    if re.match(r'^[🇺🇸🇬🇧🇩🇪\s]+ - Closed$', summary):
        # Get holiday name
        holiday_name = HOLIDAY_NAMES.get(month_day, '')
        
        if holiday_name:
            # Replace summary
            flags = re.findall(r'[🇺🇸🇬🇧🇩🇪]', summary)
            flag_str = ''.join(flags)
            new_summary = f"{flag_str} {holiday_name} - Closed"
            event_text = event_text.replace(f'SUMMARY:{summary}', f'SUMMARY:{new_summary}')
    
    return event_text

# Fix all events
fixed_events = []
for event in event_texts:
    fixed_event = fix_event(event)
    fixed_events.append(fixed_event)

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(fixed_events))
    f.write(footer)

print("Fixed missing holiday names")

# Now validate German holidays
print("\nValidating German holidays...")
de_events_by_year = defaultdict(list)

for event in fixed_events:
    # Check if this is truly a German holiday (not just combined)
    cat_match = re.search(r'CATEGORIES:(.*)', event)
    date_match = re.search(r'DTSTART[^:]*:(\d{4})(\d{4})', event)
    summary_match = re.search(r'SUMMARY:(.*)', event)
    
    if cat_match and date_match and summary_match:
        categories = cat_match.group(1)
        year = int(date_match.group(1))
        date = date_match.group(1) + date_match.group(2)
        summary = summary_match.group(1)
        
        # Check if it has German holiday name in summary
        if any(name in summary for name in ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
                                              'Weihnachtstag', 'Heiligabend', 'Silvester']):
            de_events_by_year[year].append(date)

for year in range(2025, 2030):
    count = len(de_events_by_year[year])
    print(f"{year}: {count} German holidays")