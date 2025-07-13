#!/usr/bin/env python3

import re
from datetime import datetime

print("Starting v4.0.4 FINAL fixes...")

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# 1. Update PRODID to v4.0.4
print("\n1. Updating PRODID to v4.0.4...")
content = content.replace('PRODID:-//Trading Holidays//Calendar v4.0.3//EN', 
                         'PRODID:-//Trading Holidays//Calendar v4.0.4//EN')

# 2. Fix UIDs: remove '-mixed' suffix
print("2. Removing '-mixed' from UIDs...")
content = content.replace('-mixed@', '@')

# 3. Add flag emojis to ALL summaries
print("3. Adding flag emojis to ALL SUMMARY lines...")

# Parse all events
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

# Flag mappings
flag_map = {
    'DE': '🇩🇪',
    'UK': '🇬🇧',
    'US': '🇺🇸'
}

fixed_events = []
flags_added = 0
missing_flags = []

for event in events:
    # Extract categories to determine which flags to use
    cat_match = re.search(r'CATEGORIES:([^,\n]+(?:,[^,\n]+)*)', event)
    if not cat_match:
        fixed_events.append(event)
        continue
    
    categories = cat_match.group(1)
    countries = []
    
    # Extract country codes
    for cat in categories.split(','):
        cat = cat.strip()
        if cat in ['DE', 'UK', 'US']:
            countries.append(cat)
    
    if not countries:
        fixed_events.append(event)
        continue
    
    # Sort countries in consistent order: DE, UK, US
    countries = sorted(set(countries), key=lambda x: ['DE', 'UK', 'US'].index(x))
    flags = ''.join(flag_map[c] for c in countries)
    
    # Check and fix SUMMARY
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1).strip()
        
        # Check if flags are missing
        has_flags = any(flag in summary for flag in ['🇩🇪', '🇬🇧', '🇺🇸'])
        
        if not has_flags:
            # Add flags at the beginning
            new_summary = f'SUMMARY:{flags} {summary}'
            event = event.replace(f'SUMMARY:{summary}', new_summary)
            flags_added += 1
            missing_flags.append(f"{flags} {summary}")
    
    fixed_events.append(event)

# Reconstruct the file
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')
header = content[:header_end]
footer = content[footer_start:]

# Apply PRODID update to header as well
header = header.replace('PRODID:-//Trading Holidays//Calendar v4.0.3//EN', 
                       'PRODID:-//Trading Holidays//Calendar v4.0.4//EN')

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(fixed_events))
    f.write(footer)

print(f"\n✅ Summary of v4.0.4 fixes:")
print(f"- Updated PRODID to v4.0.4")
print(f"- Removed '-mixed' from all UIDs")
print(f"- Added flags to {flags_added} SUMMARY lines")

if missing_flags:
    print(f"\nEvents that were missing flags:")
    for mf in missing_flags[:5]:
        print(f"  - {mf}")
    if len(missing_flags) > 5:
        print(f"  ... and {len(missing_flags) - 5} more")

# Verify the fixes
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    final_content = f.read()

# Check counts
prodid_check = 'v4.0.4' in final_content
mixed_count = final_content.count('-mixed')
no_flag_count = len(re.findall(r'SUMMARY:(?![🇩🇪🇬🇧🇺🇸])[^:]+(?:Closed|Early Close)', final_content))

print("\n📊 Final verification:")
print(f"- PRODID v4.0.4: {'✅' if prodid_check else '❌'}")
print(f"- Remaining '-mixed' in UIDs: {mixed_count} {'✅' if mixed_count == 0 else '❌'}")
print(f"- Summaries without flags: {no_flag_count} {'✅' if no_flag_count == 0 else '❌'}")