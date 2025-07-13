#!/usr/bin/env python3

import re
from datetime import datetime

print("Starting v4.0.2 fixes...")

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# 1. Remove Tag der Deutschen Einheit (Oct 3, 2027)
print("\n1. Removing incorrect Tag der Deutschen Einheit...")
# Find and remove the entire event
pattern = r'BEGIN:VEVENT\s*\nDTSTART;VALUE=DATE:20271003.*?END:VEVENT\s*\n'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 2. Update PRODID to v4.0.1
print("2. Updating PRODID to v4.0.1...")
content = content.replace('PRODID:-//Trading Holidays//Calendar v4.0.0//EN', 
                         'PRODID:-//Trading Holidays//Calendar v4.0.1//EN')

# 3. Convert Early Close events to All-Day format
print("3. Converting Early Close events to All-Day format...")
# Find all early close events
early_close_pattern = r'(BEGIN:VEVENT\s*\n)(DTSTART;TZID=[^:]+:(\d{8})T\d{6}\s*\nDTEND;TZID=[^:]+:\d{8}T\d{6}\s*\n)(.*?)(SUMMARY:.*?Early Close.*?\n)(.*?)(END:VEVENT)'

def convert_to_all_day(match):
    begin = match.group(1)
    date = match.group(3)
    middle = match.group(4)
    summary = match.group(5)
    rest = match.group(6)
    end = match.group(7)
    
    # Replace datetime with date-only format
    new_dtstart = f'DTSTART;VALUE=DATE:{date}\n'
    
    # Update VALARM text if present
    rest = rest.replace('Markets closed today', 'Markets close early at 1:00 PM ET')
    
    return begin + new_dtstart + middle + summary + rest + end

content = re.sub(early_close_pattern, convert_to_all_day, content, flags=re.DOTALL)

# 4. Add missing flag emojis
print("4. Adding missing flag emojis...")

# Map of flag patterns
flag_map = {
    'DE,UK,US': '🇩🇪🇬🇧🇺🇸',
    'DE,UK': '🇩🇪🇬🇧', 
    'DE,US': '🇩🇪🇺🇸',
    'UK,US': '🇬🇧🇺🇸',
    'DE': '🇩🇪',
    'UK': '🇬🇧',
    'US': '🇺🇸'
}

# Function to add flags to summary
def add_flags_to_summary(event_text):
    # Extract categories
    cat_match = re.search(r'CATEGORIES:([A-Z,]+),', event_text)
    if not cat_match:
        return event_text
    
    categories = cat_match.group(1)
    flags = flag_map.get(categories, '')
    
    if not flags:
        return event_text
    
    # Check if flags already exist in summary
    if any(flag in event_text for flag in ['🇩🇪', '🇬🇧', '🇺🇸']):
        return event_text
    
    # Add flags to summary
    event_text = re.sub(r'(SUMMARY:)(.+)', rf'\1{flags} \2', event_text)
    
    return event_text

# Process all events
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)
fixed_events = []

for event in events:
    fixed_event = add_flags_to_summary(event)
    fixed_events.append(fixed_event)

# Reconstruct content
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')
header = content[:header_end]
footer = content[footer_start:]

# 5. Combine Dec 24 events where DE is closed and US has early close
print("5. Combining Dec 24 events...")

# Group events by date
events_by_date = {}
for event in fixed_events:
    date_match = re.search(r'DTSTART;VALUE=DATE:(\d{8})', event)
    if date_match:
        date = date_match.group(1)
        if date not in events_by_date:
            events_by_date[date] = []
        events_by_date[date].append(event)

# Process each date
final_events = []
for date, date_events in sorted(events_by_date.items()):
    if date.endswith('1224'):  # December 24
        # Check if we have both DE closed and US early close
        de_event = None
        us_early = None
        other_events = []
        
        for event in date_events:
            if 'Heiligabend' in event and 'CATEGORIES:DE,' in event:
                de_event = event
            elif 'Christmas Eve - Early Close' in event and 'CATEGORIES:US,' in event:
                us_early = event
            else:
                other_events.append(event)
        
        if de_event and us_early:
            # Combine them
            combined = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{date}-de-us-mixed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪🇺🇸 Heiligabend / Christmas Eve - DE Closed, US Early Close 1PM
DESCRIPTION:German stock markets closed all day. US commodity futures markets close at 12:00 PM CT / 1:00 PM ET
CATEGORIES:DE,US,Mixed
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: DE closed, US early close at 1:00 PM ET
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
            final_events.append(combined)
            final_events.extend(other_events)
        else:
            # Keep all events as-is
            final_events.extend(date_events)
    else:
        # Keep all events for this date
        final_events.extend(date_events)

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(final_events))
    f.write(footer)

# Count final events
final_count = len(final_events)
print(f"\nFinal event count: {final_count} (should be ~97-98)")

# Summary of changes
print("\n✅ Summary of changes:")
print("- Removed Tag der Deutschen Einheit (Oct 3, 2027)")
print("- Updated PRODID to v4.0.1")
print("- Converted Early Close events to All-Day format")
print("- Added missing flag emojis")
print("- Combined Dec 24 events where applicable")