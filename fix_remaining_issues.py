#!/usr/bin/env python3

import re
from datetime import datetime

# Holiday names for remaining missing dates
MISSING_HOLIDAY_NAMES = {
    '0619': 'Juneteenth',
    '0119': 'Martin Luther King Jr. Day',
    '0118': 'Martin Luther King Jr. Day',
    '0117': 'Martin Luther King Jr. Day',
    '0115': 'Martin Luther King Jr. Day',
    '0221': 'Presidents\' Day',
    '0504': 'Early May Bank Holiday',
    '0503': 'Early May Bank Holiday',
    '0618': 'Juneteenth',
    '0705': 'Independence Day',
    '1122': 'Thanksgiving',
}

# Read file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

# Fix missing holiday names
for month_day, holiday_name in MISSING_HOLIDAY_NAMES.items():
    # Find events with missing names on this date
    pattern = rf'(DTSTART[^:]*:\d{{4}}{month_day}.*?SUMMARY:[🇺🇸🇬🇧]+\s*-\s*Closed)'
    
    def replace_summary(match):
        full_match = match.group(0)
        # Extract the flag
        flag_match = re.search(r'SUMMARY:([🇺🇸🇬🇧]+)\s*-\s*Closed', full_match)
        if flag_match:
            flag = flag_match.group(1)
            return full_match.replace(f'SUMMARY:{flag}  - Closed', f'SUMMARY:{flag} {holiday_name} - Closed')
        return full_match
    
    content = re.sub(pattern, replace_summary, content, flags=re.DOTALL)

# Write back
with open('Trading-Holidays-2025-2029-Combined.ics', 'w') as f:
    f.write(content)

print("Fixed remaining missing holiday names")

# Now let's also create a proper German holiday validation
print("\nValidating actual German holidays:")
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

# German holidays should be exactly these 8 per year:
# 1. Neujahr (New Year's Day)
# 2. Karfreitag (Good Friday)
# 3. Ostermontag (Easter Monday)
# 4. Tag der Arbeit (May Day)
# 5. 1. Weihnachtstag (Christmas Day)
# 6. 2. Weihnachtstag (Boxing Day)
# 7. Heiligabend (Christmas Eve)
# 8. Silvester (New Year's Eve)

de_holidays_by_year = {year: [] for year in range(2025, 2030)}

for event in events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    date_match = re.search(r'DTSTART[^:]*:(\d{8})', event)
    
    if summary_match and date_match:
        summary = summary_match.group(1)
        date = date_match.group(1)
        year = int(date[:4])
        
        # Check if this is a German holiday by looking for German names
        german_holidays = ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
                          '1. Weihnachtstag', '2. Weihnachtstag', 'Heiligabend', 'Silvester']
        
        for holiday in german_holidays:
            if holiday in summary:
                de_holidays_by_year[year].append((date, holiday))
                break

# Print results
for year in sorted(de_holidays_by_year.keys()):
    holidays = de_holidays_by_year[year]
    print(f"\n{year}: {len(holidays)} German holidays")
    for date, name in sorted(holidays):
        print(f"  {date}: {name}")
    
    # Check what's missing
    expected = ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
                '1. Weihnachtstag', '2. Weihnachtstag', 'Heiligabend', 'Silvester']
    found = [name for _, name in holidays]
    missing = [h for h in expected if h not in found]
    if missing:
        print(f"  Missing: {', '.join(missing)}")