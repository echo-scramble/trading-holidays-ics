#!/usr/bin/env python3

import re
from datetime import datetime

# Read the fixed file
with open('Trading-Holidays-2025-2029-Combined-FIXED.ics', 'r') as f:
    content = f.read()

# Find all early close events
early_close_pattern = r'(BEGIN:VEVENT.*?Early Close.*?END:VEVENT)'
events = re.findall(early_close_pattern, content, re.DOTALL)

print(f"Found {len(events)} early close events")

# Convert each early close event
for event in events:
    # Extract date
    date_match = re.search(r'DTSTART;VALUE=DATE:(\d{8})', event)
    if date_match:
        date_str = date_match.group(1)
        
        # Create datetime strings
        # Market opens at 9:30 AM ET, closes early at 1:00 PM ET
        start_time = f"DTSTART;TZID=America/New_York:{date_str}T093000"
        end_time = f"DTEND;TZID=America/New_York:{date_str}T130000"
        
        # Replace DATE with DATETIME
        new_event = event.replace(f'DTSTART;VALUE=DATE:{date_str}', start_time)
        
        # Add DTEND after DTSTART
        new_event = re.sub(
            r'(DTSTART;TZID=America/New_York:\d{8}T\d{6})',
            r'\1\n' + end_time,
            new_event
        )
        
        # Update description to be more specific
        new_event = re.sub(
            r'DESCRIPTION:.*',
            'DESCRIPTION:US commodity futures markets close early at 12:00 PM CT / 1:00 PM ET',
            new_event
        )
        
        # Replace in content
        content = content.replace(event, new_event)

# Handle special case: Christmas Eve mixed events (DE closed, US early)
mixed_pattern = r'(BEGIN:VEVENT.*?Christmas Eve.*?Mixed.*?END:VEVENT)'
mixed_events = re.findall(mixed_pattern, content, re.DOTALL)

print(f"Found {len(mixed_events)} mixed Christmas Eve events")

for event in mixed_events:
    # For mixed events, we need to split into two events
    date_match = re.search(r'DTSTART;VALUE=DATE:(\d{8})', event)
    uid_match = re.search(r'UID:(.*)', event)
    
    if date_match and uid_match:
        date_str = date_match.group(1)
        base_uid = uid_match.group(1).strip()
        
        # Create DE full day event
        de_event = f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{date_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{base_uid}-de
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
        
        # Create US early close event
        us_event = f"""BEGIN:VEVENT
DTSTART;TZID=America/New_York:{date_str}T093000
DTEND;TZID=America/New_York:{date_str}T130000
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{base_uid}-us
SEQUENCE:1
SUMMARY:🇺🇸 Christmas Eve - Early Close
DESCRIPTION:US commodity futures markets close early at 12:00 PM CT / 1:00 PM ET
CATEGORIES:US,Early Close
TRANSP:TRANSPARENT
END:VEVENT"""
        
        # Replace mixed event with two separate events
        content = content.replace(event, de_event + '\n' + us_event)

# Write the final corrected file
with open('Trading-Holidays-2025-2029-Combined-FINAL.ics', 'w') as f:
    f.write(content)

# Count final events
final_events = content.count('BEGIN:VEVENT')
print(f"Final file has {final_events} events")