#!/usr/bin/env python3

import re
from datetime import datetime

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# 1. Fix misleading summaries for 2027
# Heiligabend (Dec 24) should not mention "Christmas Day"
content = content.replace(
    'SUMMARY:🇩🇪🇺🇸 Heiligabend / Christmas Day - Closed',
    'SUMMARY:🇩🇪🇺🇸 Heiligabend / Christmas Eve - Closed'
)

# Silvester (Dec 31) should not mention "New Year's Day"
content = content.replace(
    'SUMMARY:🇩🇪🇺🇸 Silvester / New Year\'s Day - Closed',
    'SUMMARY:🇩🇪🇺🇸 Silvester / New Year\'s Eve - Closed'
)

# 2. Add missing VALARM blocks to Christmas Eve Early Close events
# Find all Christmas Eve Early Close events without VALARM
pattern = r'(BEGIN:VEVENT.*?SUMMARY:🇺🇸 Christmas Eve - Early Close.*?TRANSP:TRANSPARENT)\s*(END:VEVENT)'

def add_valarm(match):
    event_content = match.group(1)
    end_vevent = match.group(2)
    
    # Check if VALARM already exists
    if 'BEGIN:VALARM' in event_content:
        return match.group(0)
    
    # Add VALARM block
    valarm = """
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM"""
    
    return f"{event_content}{valarm}\n{end_vevent}"

content = re.sub(pattern, add_valarm, content, flags=re.DOTALL)

# 3. Add missing Tag der Deutschen Einheit for 2027 (Oct 3)
# Find where to insert it (after Labor Day 2027)
insert_after = re.search(r'(UID:20270906-us-closed@trading-holidays\.com.*?END:VEVENT)', content, re.DOTALL)

if insert_after:
    new_event = f"""
BEGIN:VEVENT
DTSTART;VALUE=DATE:20271003
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:20271003-de-closed@trading-holidays.com
SEQUENCE:1
SUMMARY:🇩🇪 Tag der Deutschen Einheit - Closed
DESCRIPTION:German stock markets closed all day
CATEGORIES:DE,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT"""
    
    # Insert after Labor Day 2027
    insert_pos = insert_after.end()
    content = content[:insert_pos] + new_event + content[insert_pos:]

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(content)

print("Fixed issues found by Gemini:")
print("1. ✅ Corrected misleading summaries for 2027 (Heiligabend/Silvester)")
print("2. ✅ Added missing VALARM blocks to Christmas Eve Early Close events")
print("3. ✅ Added missing Tag der Deutschen Einheit (Oct 3, 2027)")
print("\nTotal events should now be: 102")