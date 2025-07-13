#!/usr/bin/env python3

import re

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Find all Christmas Eve Early Close events and add VALARM if missing
# Pattern to find Christmas Eve Early Close events
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

fixed_events = []
valarm_added = 0

for event in events:
    if 'Christmas Eve - Early Close' in event and 'BEGIN:VALARM' not in event:
        # Add VALARM block before END:VEVENT
        event = event.replace(
            'END:VEVENT',
            '''BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT'''
        )
        valarm_added += 1
    fixed_events.append(event)

# Reconstruct the file
# Find header and footer
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')
header = content[:header_end]
footer = content[footer_start:]

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(fixed_events))
    f.write(footer)

print(f"Added VALARM blocks to {valarm_added} Christmas Eve Early Close events")