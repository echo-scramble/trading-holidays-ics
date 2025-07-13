#!/usr/bin/env python3

import re

print("Starting v4.0.3 final fixes...")

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# 1. Update PRODID to v4.0.2
print("\n1. Updating PRODID to v4.0.2...")
content = content.replace('PRODID:-//Trading Holidays//Calendar v4.0.1//EN', 
                         'PRODID:-//Trading Holidays//Calendar v4.0.2//EN')

# 2. Fix UIDs: ice-uk -> uk
print("2. Standardizing UK UIDs from 'ice-uk' to 'uk'...")
content = content.replace('-ice-uk-', '-uk-')

# 3. Replace 'Mixed' category with 'Full Day,Early Close'
print("3. Replacing 'Mixed' category...")
content = content.replace('CATEGORIES:DE,US,Mixed', 'CATEGORIES:DE,US,Full Day,Early Close')

# 4. Add missing flag emojis
print("4. Fixing missing flag emojis in SUMMARY lines...")

# Parse all events
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

# Flag mappings
flag_map = {
    'DE,UK,US': '🇩🇪🇬🇧🇺🇸',
    'DE,UK': '🇩🇪🇬🇧', 
    'DE,US': '🇩🇪🇺🇸',
    'UK,US': '🇬🇧🇺🇸',
    'DE': '🇩🇪',
    'UK': '🇬🇧',
    'US': '🇺🇸'
}

fixed_events = []
flags_fixed = 0

for event in events:
    # Extract categories to determine which flags to use
    cat_match = re.search(r'CATEGORIES:([A-Z,]+)', event)
    if not cat_match:
        fixed_events.append(event)
        continue
    
    # Extract just the country codes
    categories = cat_match.group(1)
    countries = []
    for cat in categories.split(','):
        if cat in ['DE', 'UK', 'US']:
            countries.append(cat)
    
    if not countries:
        fixed_events.append(event)
        continue
    
    # Get the right flags
    country_str = ','.join(sorted(countries, key=lambda x: ['DE', 'UK', 'US'].index(x)))
    flags = flag_map.get(country_str, '')
    
    if not flags:
        fixed_events.append(event)
        continue
    
    # Check if SUMMARY already has flags
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1)
        
        # If no flags present, add them
        if not any(flag in summary for flag in ['🇩🇪', '🇬🇧', '🇺🇸']):
            # Add flags at the beginning of summary
            new_summary = f'SUMMARY:{flags} {summary.strip()}'
            event = event.replace(f'SUMMARY:{summary}', new_summary)
            flags_fixed += 1
    
    fixed_events.append(event)

# Reconstruct the file
header_end = content.find('BEGIN:VEVENT')
footer_start = content.rfind('END:VEVENT') + len('END:VEVENT')
header = content[:header_end]
footer = content[footer_start:]

# Apply the fixed PRODID and UID changes to header
header = header.replace('PRODID:-//Trading Holidays//Calendar v4.0.1//EN', 
                       'PRODID:-//Trading Holidays//Calendar v4.0.2//EN')

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(header)
    f.write('\n'.join(fixed_events))
    f.write(footer)

print(f"\n✅ Summary of v4.0.3 fixes:")
print(f"- Updated PRODID to v4.0.2")
print(f"- Standardized all 'ice-uk' UIDs to 'uk'")
print(f"- Replaced 'Mixed' category with 'Full Day,Early Close'")
print(f"- Added flags to {flags_fixed} SUMMARY lines")

# Verify the fixes
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    final_content = f.read()

# Check counts
prodid_check = 'v4.0.2' in final_content
ice_uk_count = final_content.count('ice-uk')
mixed_count = final_content.count('Mixed')
no_flag_summaries = len(re.findall(r'SUMMARY:(?![🇩🇪🇬🇧🇺🇸])', final_content))

print("\n📊 Verification:")
print(f"- PRODID v4.0.2: {'✅' if prodid_check else '❌'}")
print(f"- Remaining 'ice-uk': {ice_uk_count} {'✅' if ice_uk_count == 0 else '❌'}")
print(f"- Remaining 'Mixed': {mixed_count} {'✅' if mixed_count == 0 else '❌'}")
print(f"- Summaries without flags: {no_flag_summaries}")