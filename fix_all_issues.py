#!/usr/bin/env python3

import re
from datetime import datetime, date, timedelta
from collections import defaultdict
import hashlib

# Read the current file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Parse all events
def parse_events(content):
    events = []
    event_blocks = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)
    
    for block in event_blocks:
        event = {}
        event['block'] = block
        
        # Extract fields
        date_match = re.search(r'DTSTART;VALUE=DATE:(\d{8})', block)
        if date_match:
            event['date'] = date_match.group(1)
            event['date_obj'] = datetime.strptime(date_match.group(1), '%Y%m%d').date()
        
        uid_match = re.search(r'UID:(.*)', block)
        if uid_match:
            event['uid'] = uid_match.group(1).strip()
            
        summary_match = re.search(r'SUMMARY:(.*)', block)
        if summary_match:
            event['summary'] = summary_match.group(1).strip()
            
        categories_match = re.search(r'CATEGORIES:(.*)', block)
        if categories_match:
            event['categories'] = categories_match.group(1).strip()
            
        desc_match = re.search(r'DESCRIPTION:(.*)', block)
        if desc_match:
            event['description'] = desc_match.group(1).strip()
            
        events.append(event)
    
    return events

# Define missing German holidays
missing_de_holidays = [
    # 2027
    {'date': '20270501', 'name': 'Tag der Arbeit', 'year': 2027},
    # 2028  
    {'date': '20281231', 'name': 'Silvester', 'year': 2028},
]

# Parse existing events
events = parse_events(content)

# Group events by date for combination
events_by_date = defaultdict(list)
for event in events:
    if 'date' in event:
        events_by_date[event['date']].append(event)

# Process events
new_events = []
processed_dates = set()

# Fix category naming
def fix_categories(cat_str):
    # Replace "ICE - UK" with "UK"
    cat_str = cat_str.replace('ICE - UK', 'UK')
    
    # Parse categories
    parts = [p.strip() for p in cat_str.split(',')]
    markets = []
    closure_type = 'Full Day'
    
    for part in parts:
        if part in ['US', 'DE', 'UK']:
            markets.append(part)
        elif part in ['Full Day', 'Early Close', 'Mixed']:
            closure_type = part
    
    # Sort markets: DE, UK, US
    market_order = {'DE': 0, 'UK': 1, 'US': 2}
    markets.sort(key=lambda x: market_order.get(x, 3))
    
    return markets, closure_type

# Generate flag string
def get_flags(markets):
    flag_map = {'DE': '🇩🇪', 'UK': '🇬🇧', 'US': '🇺🇸'}
    return ''.join(flag_map.get(m, '') for m in markets)

# Generate combined summary
def generate_summary(date_str, markets, closure_type='Closed'):
    date_obj = datetime.strptime(date_str, '%Y%m%d').date()
    
    # Holiday names by market and date
    holiday_names = {
        # Good Friday
        ('0418', 'DE'): 'Karfreitag',
        ('0418', 'UK'): 'Good Friday', 
        ('0418', 'US'): 'Good Friday',
        ('0403', 'DE'): 'Karfreitag',
        ('0403', 'UK'): 'Good Friday',
        ('0403', 'US'): 'Good Friday',
        ('0326', 'DE'): 'Karfreitag',
        ('0326', 'UK'): 'Good Friday',
        ('0326', 'US'): 'Good Friday',
        ('0414', 'DE'): 'Karfreitag',
        ('0414', 'UK'): 'Good Friday',
        ('0414', 'US'): 'Good Friday',
        ('0330', 'DE'): 'Karfreitag',
        ('0330', 'UK'): 'Good Friday',
        ('0330', 'US'): 'Good Friday',
        # Easter Monday
        ('0421', 'DE'): 'Ostermontag',
        ('0421', 'UK'): 'Easter Monday',
        ('0406', 'DE'): 'Ostermontag',
        ('0406', 'UK'): 'Easter Monday',
        ('0329', 'DE'): 'Ostermontag',
        ('0329', 'UK'): 'Easter Monday',
        ('0417', 'DE'): 'Ostermontag',
        ('0417', 'UK'): 'Easter Monday',
        ('0402', 'DE'): 'Ostermontag',
        ('0402', 'UK'): 'Easter Monday',
        # Christmas
        ('1225', 'DE'): '1. Weihnachtstag',
        ('1225', 'UK'): 'Christmas Day',
        ('1225', 'US'): 'Christmas Day',
        # Boxing Day
        ('1226', 'DE'): '2. Weihnachtstag',
        ('1226', 'UK'): 'Boxing Day',
        ('1228', 'DE'): '2. Weihnachtstag',
        ('1228', 'UK'): 'Boxing Day',
        # New Year
        ('0101', 'DE'): 'Neujahr',
        ('0101', 'UK'): "New Year's Day",
        ('0101', 'US'): "New Year's Day",
        ('0103', 'UK'): "New Year's Day",
        # May Day
        ('0501', 'DE'): 'Tag der Arbeit',
        ('0501', 'UK'): 'Early May Bank Holiday',
        # Memorial Day / Spring Bank
        ('0526', 'US'): 'Memorial Day',
        ('0526', 'UK'): 'Spring Bank Holiday',
        ('0525', 'US'): 'Memorial Day', 
        ('0525', 'UK'): 'Spring Bank Holiday',
        ('0531', 'US'): 'Memorial Day',
        ('0531', 'UK'): 'Spring Bank Holiday',
        ('0529', 'US'): 'Memorial Day',
        ('0529', 'UK'): 'Spring Bank Holiday',
        ('0528', 'US'): 'Memorial Day',
        ('0528', 'UK'): 'Spring Bank Holiday',
    }
    
    # Get month-day
    mmdd = date_str[4:]
    
    # Build holiday names
    names = []
    for market in markets:
        name = holiday_names.get((mmdd, market))
        if name and name not in names:
            names.append(name)
    
    # Format summary
    flags = get_flags(markets)
    if len(names) > 1:
        name_str = ' / '.join(names)
    elif names:
        name_str = names[0]
    else:
        # Fallback - extract from existing summaries
        name_str = 'Holiday'
    
    if 'Early Close' in closure_type:
        status = 'Early Close 1PM'
    elif closure_type == 'Mixed':
        status = 'Mixed'
    else:
        status = 'Closed'
        
    return f"{flags} {name_str} - {status}"

# Generate description
def generate_description(markets, closure_type='Full Day'):
    market_names = {
        'DE': 'German stock markets',
        'UK': 'ICE Futures Europe (Brent)',
        'US': 'US commodity futures markets'
    }
    
    parts = [market_names[m] for m in markets if m in market_names]
    
    if len(parts) > 1:
        desc = ', '.join(parts[:-1]) + ' and ' + parts[-1]
    else:
        desc = parts[0] if parts else 'Markets'
        
    if 'Early Close' in closure_type:
        desc += ' close at 12:00 PM CT / 1:00 PM ET'
    else:
        desc += ' closed all day'
        
    return desc

# Process each date
for date_str, date_events in sorted(events_by_date.items()):
    if date_str in processed_dates:
        continue
        
    # Check if we need to combine events
    if len(date_events) > 1 or any('ICE - UK' in e.get('categories', '') for e in date_events):
        # Combine events
        all_markets = set()
        closure_types = set()
        
        # Keep the first UID (prefer US or DE over UK standalone)
        uid = None
        for e in sorted(date_events, key=lambda x: 0 if 'US' in x.get('categories', '') else 1 if 'DE' in x.get('categories', '') else 2):
            if not uid:
                uid = e.get('uid')
            
            markets, closure = fix_categories(e.get('categories', ''))
            all_markets.update(markets)
            closure_types.add(closure)
        
        # Determine final closure type
        if len(closure_types) > 1 and 'Early Close' in closure_types and 'Full Day' in closure_types:
            closure_type = 'Mixed'
        else:
            closure_type = list(closure_types)[0] if closure_types else 'Full Day'
            
        # Sort markets
        markets = sorted(list(all_markets), key=lambda x: {'DE': 0, 'UK': 1, 'US': 2}.get(x, 3))
        
        # Generate new event
        new_summary = generate_summary(date_str, markets, closure_type)
        new_desc = generate_description(markets, closure_type)
        new_categories = ','.join(markets) + ',' + closure_type
        
        # Create event text
        event_text = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{uid}
SEQUENCE:1
SUMMARY:{new_summary}
DESCRIPTION:{new_desc}
CATEGORIES:{new_categories}
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
        
        new_events.append(event_text)
        processed_dates.add(date_str)
        
    else:
        # Single event - just fix categories and add flags
        event = date_events[0]
        markets, closure_type = fix_categories(event.get('categories', ''))
        
        # Skip if it's an early close event (handle separately)
        if 'Early Close' in closure_type:
            # Keep original for now, will convert to DATETIME later
            new_events.append(event['block'])
        else:
            new_summary = generate_summary(date_str, markets, closure_type)
            new_desc = generate_description(markets, closure_type)
            new_categories = ','.join(markets) + ',' + closure_type
            
            # Update event
            updated_block = event['block']
            updated_block = re.sub(r'SUMMARY:.*', f'SUMMARY:{new_summary}', updated_block)
            updated_block = re.sub(r'DESCRIPTION:.*', f'DESCRIPTION:{new_desc}', updated_block)
            updated_block = re.sub(r'CATEGORIES:.*', f'CATEGORIES:{new_categories}', updated_block)
            updated_block = re.sub(r'DTSTAMP:.*', f'DTSTAMP:{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}', updated_block)
            
            # Add SEQUENCE if modified
            if 'SEQUENCE:' not in updated_block:
                updated_block = updated_block.replace('SUMMARY:', 'SEQUENCE:1\nSUMMARY:')
                
            new_events.append(updated_block)
        
        processed_dates.add(date_str)

# Add missing German holidays
for holiday in missing_de_holidays:
    date_str = holiday['date']
    if date_str not in processed_dates:
        # Check if it should be combined with other markets
        year = holiday['year']
        date_obj = datetime.strptime(date_str, '%Y%m%d').date()
        
        # Generate UID
        uid = f"{date_str}-de-closed@trading-holidays.com"
        
        # Create event
        if holiday['name'] == 'Tag der Arbeit':
            summary = "🇩🇪 Tag der Arbeit (Labour Day) - Closed"
        else:
            summary = f"🇩🇪 {holiday['name']} (New Year's Eve) - Closed"
            
        event_text = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{uid}
SUMMARY:{summary}
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
        
        new_events.append(event_text)

# Update header
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

# Sort events by date
def get_event_date(event_text):
    match = re.search(r'DTSTART[^:]*:(\d{8})', event_text)
    return match.group(1) if match else '99999999'

new_events.sort(key=get_event_date)

# Write the corrected file
with open('Trading-Holidays-2025-2029-Combined-FIXED.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(new_events))
    f.write('\nEND:VCALENDAR')

print(f"Fixed file created with {len(new_events)} events")