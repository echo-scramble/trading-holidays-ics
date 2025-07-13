#!/usr/bin/env python3

import re
from datetime import datetime, date
from collections import defaultdict

# Read the backup file
with open('Trading-Holidays-2025-2029-Combined.ics.backup', 'r') as f:
    content = f.read()

# Parse all events into structured data
def parse_event(event_text):
    event = {'raw': event_text}
    
    # Extract all fields
    fields = {
        'dtstart': r'DTSTART[^:]*:(.*)',
        'dtend': r'DTEND[^:]*:(.*)',
        'uid': r'UID:(.*)',
        'summary': r'SUMMARY:(.*)',
        'description': r'DESCRIPTION:(.*)',
        'categories': r'CATEGORIES:(.*)',
        'sequence': r'SEQUENCE:(.*)',
    }
    
    for field, pattern in fields.items():
        match = re.search(pattern, event_text)
        if match:
            event[field] = match.group(1).strip()
    
    # Parse date
    if 'dtstart' in event:
        if 'VALUE=DATE:' in event_text:
            date_match = re.search(r'VALUE=DATE:(\d{8})', event_text)
            if date_match:
                event['date'] = date_match.group(1)
                event['date_type'] = 'DATE'
        else:
            date_match = re.search(r'DTSTART[^:]*:(\d{8})', event['dtstart'])
            if date_match:
                event['date'] = date_match.group(1)
                event['date_type'] = 'DATETIME'
    
    return event

# Extract all events
event_texts = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)
events = [parse_event(et) for et in event_texts]

print(f"Parsed {len(events)} events")

# Group by date
events_by_date = defaultdict(list)
for event in events:
    if 'date' in event:
        events_by_date[event['date']].append(event)

# Define all holidays with proper mappings
holiday_info = {
    # New Year's Day
    '20250101': {'markets': ['US', 'UK'], 'name': {"US": "New Year's Day", "UK": "New Year's Day"}},
    '20260101': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Neujahr", "US": "New Year's Day", "UK": "New Year's Day"}},
    '20270101': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Neujahr", "US": "New Year's Day", "UK": "New Year's Day"}},
    '20280103': {'markets': ['UK'], 'name': {"UK": "New Year's Day"}},  # UK observed
    '20290101': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Neujahr", "US": "New Year's Day", "UK": "New Year's Day"}},
    
    # Good Friday - all markets
    '20250418': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Karfreitag", "US": "Good Friday", "UK": "Good Friday"}},
    '20260403': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Karfreitag", "US": "Good Friday", "UK": "Good Friday"}},
    '20270326': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Karfreitag", "US": "Good Friday", "UK": "Good Friday"}},
    '20280414': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Karfreitag", "US": "Good Friday", "UK": "Good Friday"}},
    '20290330': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "Karfreitag", "US": "Good Friday", "UK": "Good Friday"}},
    
    # Easter Monday - DE + UK
    '20250421': {'markets': ['DE', 'UK'], 'name': {"DE": "Ostermontag", "UK": "Easter Monday"}},
    '20260406': {'markets': ['DE', 'UK'], 'name': {"DE": "Ostermontag", "UK": "Easter Monday"}},
    '20270329': {'markets': ['DE', 'UK'], 'name': {"DE": "Ostermontag", "UK": "Easter Monday"}},
    '20280417': {'markets': ['DE', 'UK'], 'name': {"DE": "Ostermontag", "UK": "Easter Monday"}},
    '20290402': {'markets': ['DE', 'UK'], 'name': {"DE": "Ostermontag", "UK": "Easter Monday"}},
    
    # May Day / Early May Bank Holiday
    '20250501': {'markets': ['DE'], 'name': {"DE": "Tag der Arbeit"}},
    '20260501': {'markets': ['DE'], 'name': {"DE": "Tag der Arbeit"}},
    '20270501': {'markets': ['DE'], 'name': {"DE": "Tag der Arbeit"}},  # Missing in original!
    '20280501': {'markets': ['DE', 'UK'], 'name': {"DE": "Tag der Arbeit", "UK": "Early May Bank Holiday"}},
    '20290501': {'markets': ['DE'], 'name': {"DE": "Tag der Arbeit"}},
    
    # Memorial Day / Spring Bank Holiday - US + UK  
    '20250526': {'markets': ['US', 'UK'], 'name': {"US": "Memorial Day", "UK": "Spring Bank Holiday"}},
    '20260525': {'markets': ['US', 'UK'], 'name': {"US": "Memorial Day", "UK": "Spring Bank Holiday"}},
    '20270531': {'markets': ['US', 'UK'], 'name': {"US": "Memorial Day", "UK": "Spring Bank Holiday"}},
    '20280529': {'markets': ['US', 'UK'], 'name': {"US": "Memorial Day", "UK": "Spring Bank Holiday"}},
    '20290528': {'markets': ['US', 'UK'], 'name': {"US": "Memorial Day", "UK": "Spring Bank Holiday"}},
    
    # Christmas Day
    '20251225': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "1. Weihnachtstag", "US": "Christmas Day", "UK": "Christmas Day"}},
    '20261225': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "1. Weihnachtstag", "US": "Christmas Day", "UK": "Christmas Day"}},
    '20271227': {'markets': ['UK'], 'name': {"UK": "Christmas Day"}},  # UK observed Mon
    '20281225': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "1. Weihnachtstag", "US": "Christmas Day", "UK": "Christmas Day"}},
    '20291225': {'markets': ['DE', 'US', 'UK'], 'name': {"DE": "1. Weihnachtstag", "US": "Christmas Day", "UK": "Christmas Day"}},
    
    # Boxing Day
    '20251226': {'markets': ['DE', 'UK'], 'name': {"DE": "2. Weihnachtstag", "UK": "Boxing Day"}},
    '20261228': {'markets': ['DE', 'UK'], 'name': {"DE": "2. Weihnachtstag", "UK": "Boxing Day"}},  # Observed Mon
    '20271228': {'markets': ['UK'], 'name': {"UK": "Boxing Day"}},  # UK observed Tue
    '20281226': {'markets': ['DE', 'UK'], 'name': {"DE": "2. Weihnachtstag", "UK": "Boxing Day"}},
    '20291226': {'markets': ['DE', 'UK'], 'name': {"DE": "2. Weihnachtstag", "UK": "Boxing Day"}},
    
    # Christmas/New Year special observances
    '20271224': {'markets': ['DE', 'US'], 'name': {"DE": "Heiligabend", "US": "Christmas Day"}},  # US observes Fri
    '20271231': {'markets': ['DE', 'US'], 'name': {"DE": "Silvester", "US": "New Year's Day"}},  # US observes Fri
    
    # Regular German year-end holidays
    '20251224': {'markets': ['DE'], 'name': {"DE": "Heiligabend"}, 'us_early': True},
    '20251231': {'markets': ['DE'], 'name': {"DE": "Silvester"}},
    '20261224': {'markets': ['DE'], 'name': {"DE": "Heiligabend"}, 'us_early': True},
    '20261231': {'markets': ['DE'], 'name': {"DE": "Silvester"}},
    '20281231': {'markets': ['DE'], 'name': {"DE": "Silvester"}},  # Missing in original!
    '20291224': {'markets': ['DE'], 'name': {"DE": "Heiligabend"}, 'us_early': True},
    '20291231': {'markets': ['DE'], 'name': {"DE": "Silvester"}},
}

# Generate new events
new_events = []
processed_dates = set()

# Helper functions
def get_flags(markets):
    flag_map = {'DE': '🇩🇪', 'UK': '🇬🇧', 'US': '🇺🇸'}
    return ''.join(flag_map[m] for m in markets)

def generate_summary(markets, names, is_early_close=False):
    flags = get_flags(markets)
    
    # Build name string
    name_parts = []
    for m in markets:
        if m in names:
            name_parts.append(names[m])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_names = []
    for name in name_parts:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
    
    name_str = ' / '.join(unique_names)
    
    if is_early_close:
        return f"{flags} {name_str} - Early Close 1PM"
    else:
        return f"{flags} {name_str} - Closed"

def generate_description(markets, is_early_close=False):
    market_names = {
        'DE': 'German stock markets',
        'UK': 'ICE Futures Europe (Brent)',
        'US': 'US commodity futures markets'
    }
    
    parts = [market_names[m] for m in markets]
    
    if len(parts) > 1:
        desc = ', '.join(parts[:-1]) + ' and ' + parts[-1]
    else:
        desc = parts[0]
    
    if is_early_close:
        desc += ' close at 12:00 PM CT / 1:00 PM ET'
    else:
        desc += ' closed all day'
    
    return desc

# Process all dates
all_dates = sorted(set(list(events_by_date.keys()) + list(holiday_info.keys())))

for date_str in all_dates:
    if date_str in processed_dates:
        continue
    
    # Get existing events for this date
    existing_events = events_by_date.get(date_str, [])
    
    # Get expected holiday info
    expected = holiday_info.get(date_str, {})
    
    # Determine actual markets and closure types
    markets = set()
    is_early_close = False
    has_us_early = False
    
    # From existing events
    for event in existing_events:
        cat = event.get('categories', '')
        if 'US' in cat and 'Early Close' in cat:
            has_us_early = True
        elif 'US' in cat:
            markets.add('US')
        if 'DE' in cat:
            markets.add('DE')
        if 'ICE - UK' in cat or 'UK' in cat:
            markets.add('UK')
    
    # From expected holidays
    if expected:
        markets.update(expected.get('markets', []))
        if expected.get('us_early'):
            has_us_early = True
    
    # Skip if no markets
    if not markets:
        continue
    
    # Sort markets
    markets = sorted(list(markets), key=lambda x: {'DE': 0, 'UK': 1, 'US': 2}[x])
    
    # Get the best UID (prefer existing combined events)
    uid = None
    for event in existing_events:
        if not uid:
            uid = event.get('uid')
        # Prefer UIDs from combined events
        cat = event.get('categories', '')
        if cat.count(',') > 2:  # Multiple markets
            uid = event.get('uid')
            break
    
    if not uid:
        # Generate new UID
        market_str = '-'.join(markets).lower()
        uid = f"{date_str}-{market_str}-closed@trading-holidays.com"
    
    # Handle mixed Christmas Eve (DE closed + US early)
    if has_us_early and 'DE' in markets:
        # Create DE full day event
        de_summary = f"🇩🇪 {expected['name']['DE']} (Christmas Eve) - Closed"
        de_event = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{date_str}-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:{de_summary}
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
        new_events.append(de_event)
        
        # Create US early close event
        us_event = f"""BEGIN:VEVENT
DTSTART;TZID=America/New_York:{date_str}T093000
DTEND;TZID=America/New_York:{date_str}T130000
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{date_str}-us-early@trading-holidays.com
SEQUENCE:1
SUMMARY:🇺🇸 Christmas Eve - Early Close
DESCRIPTION:US commodity futures markets close at 12:00 PM CT / 1:00 PM ET
CATEGORIES:US,Early Close
TRANSP:TRANSPARENT
END:VEVENT"""
        new_events.append(us_event)
        
    else:
        # Regular combined event
        names = expected.get('name', {})
        
        # Fill in missing names from existing events
        if not names:
            for event in existing_events:
                summary = event.get('summary', '')
                # Extract holiday name from summary
                if 'Tag der Arbeit' in summary:
                    names['DE'] = 'Tag der Arbeit'
                elif 'Labour Day' in summary and 'US' in markets:
                    names['US'] = 'Labor Day'
                # Add more patterns as needed
        
        summary = generate_summary(markets, names)
        description = generate_description(markets)
        categories = ','.join(markets) + ',Full Day'
        
        event_text = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{uid}
SEQUENCE:1
SUMMARY:{summary}
DESCRIPTION:{description}
CATEGORIES:{categories}
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
        new_events.append(event_text)
    
    processed_dates.add(date_str)

# Add remaining events (US-only holidays, early closes, etc.)
for date_str, existing_events in events_by_date.items():
    if date_str not in processed_dates:
        for event in existing_events:
            if 'Early Close' in event.get('categories', ''):
                # Convert to DATETIME format
                event_text = event['raw']
                
                # Replace DATE with DATETIME
                event_text = re.sub(
                    r'DTSTART;VALUE=DATE:(\d{8})',
                    r'DTSTART;TZID=America/New_York:\1T093000\nDTEND;TZID=America/New_York:\1T130000',
                    event_text
                )
                
                # Update DTSTAMP
                event_text = re.sub(
                    r'DTSTAMP:.*',
                    f'DTSTAMP:{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}',
                    event_text
                )
                
                # Add SEQUENCE
                if 'SEQUENCE:' not in event_text:
                    event_text = event_text.replace('UID:', 'SEQUENCE:1\nUID:')
                
                # Fix summary to include flag
                event_text = re.sub(
                    r'SUMMARY:([^🇺🇸])',
                    r'SUMMARY:🇺🇸 \1',
                    event_text
                )
                
                new_events.append(event_text)
            else:
                # Keep as-is but update DTSTAMP and add SEQUENCE
                event_text = event['raw']
                
                # Update DTSTAMP
                event_text = re.sub(
                    r'DTSTAMP:.*',
                    f'DTSTAMP:{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}',
                    event_text
                )
                
                # Add SEQUENCE
                if 'SEQUENCE:' not in event_text:
                    event_text = event_text.replace('UID:', 'SEQUENCE:1\nUID:')
                
                # Fix categories
                event_text = event_text.replace('ICE - UK', 'UK')
                
                # Add flag if missing
                if '🇺🇸' not in event_text and 'US' in event.get('categories', ''):
                    event_text = re.sub(
                        r'SUMMARY:([^🇺🇸])',
                        r'SUMMARY:🇺🇸 \1',
                        event_text
                    )
                
                new_events.append(event_text)

# Sort events by date
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

new_events.sort(key=extract_date)

# Create the final header
header = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Trading Holidays//Calendar v4.0.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Trading Holidays 2025-2029
X-WR-CALDESC:US (NYMEX/CME) commodity futures, German (Xetra) stock market, and UK (ICE Futures Europe) trading holidays and early closures
BEGIN:VTIMEZONE
TZID:America/New_York
TZURL:http://tzurl.org/zoneinfo-outlook/America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VTIMEZONE
TZID:Europe/Berlin
TZURL:http://tzurl.org/zoneinfo-outlook/Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VTIMEZONE
TZID:Europe/London
TZURL:http://tzurl.org/zoneinfo-outlook/Europe/London
X-LIC-LOCATION:Europe/London
BEGIN:DAYLIGHT
TZOFFSETFROM:+0000
TZOFFSETTO:+0100
TZNAME:BST
DTSTART:19700329T010000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0100
TZOFFSETTO:+0000
TZNAME:GMT
DTSTART:19701025T020000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
"""

# Write the final file
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(new_events))
    f.write('\nEND:VCALENDAR')

print(f"Created final file with {len(new_events)} events")

# Quick validation
de_count_by_year = defaultdict(int)
for event in new_events:
    if ',DE,' in event or event.endswith(',DE,Full Day'):
        match = re.search(r'DTSTART[^:]*:(\d{4})', event)
        if match:
            year = int(match.group(1))
            de_count_by_year[year] += 1

print("\nDE holidays per year:")
for year in sorted(de_count_by_year.keys()):
    print(f"{year}: {de_count_by_year[year]}")