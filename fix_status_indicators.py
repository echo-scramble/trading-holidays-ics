#!/usr/bin/env python3

import re
from datetime import datetime

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Count changes for logging
geschlossen_count = content.count('Geschlossen')  # Count German "Geschlossen" to replace with "Closed"
early_close_no_time_count = len(re.findall(r'SUMMARY:.*Early Close\s*$', content, re.MULTILINE))

print(f"Found {geschlossen_count} instances of 'Geschlossen'")
print(f"Found {early_close_no_time_count} instances of 'Early Close' without time")

# 1. Replace "Geschlossen" with "Closed"
content = content.replace('Geschlossen', 'Closed')

# 2. Fix "Early Close" without time -> "Early Close 1PM"
# Need to be careful to only match summaries that end with "Early Close"
content = re.sub(
    r'(SUMMARY:.*Early Close)\s*$',
    r'\1 1PM',
    content,
    flags=re.MULTILINE
)

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(content)

print("\nChanges applied:")
print(f"- Replaced {geschlossen_count} instances of 'Geschlossen' with 'Closed'")
print(f"- Added '1PM' to {early_close_no_time_count} 'Early Close' entries")

# Verify changes
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    updated_content = f.read()

# Check if any Geschlossen remains
remaining_geschlossen = updated_content.count('Geschlossen')
if remaining_geschlossen > 0:
    print(f"\n⚠️ WARNING: {remaining_geschlossen} instances of 'Geschlossen' still remain!")
else:
    print("\n✅ All 'Geschlossen' replaced successfully")

# Check Early Close consistency
early_close_pattern = re.findall(r'SUMMARY:.*Early Close.*', updated_content)
early_close_no_time = [ec for ec in early_close_pattern if not re.search(r'Early Close \d+[AP]M', ec)]
if early_close_no_time:
    print(f"\n⚠️ WARNING: {len(early_close_no_time)} 'Early Close' entries still without time:")
    for ec in early_close_no_time[:3]:
        print(f"  - {ec}")
else:
    print("✅ All 'Early Close' entries now have time specified")