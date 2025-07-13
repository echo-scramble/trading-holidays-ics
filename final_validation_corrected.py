#!/usr/bin/env python3

import re
from collections import defaultdict

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

print("# Final Validation Report\n")

# Count events
events = re.findall(r'BEGIN:VEVENT', content)
print(f"Total events: {len(events)}")

# Check header
if 'PRODID:-//Trading Holidays//Calendar v4.0.0//EN' in content:
    print("✅ PRODID: v4.0.0")
else:
    print("❌ PRODID not updated")

if 'UK (ICE Futures Europe)' in content:
    print("✅ Description includes UK")
else:
    print("❌ Description missing UK")

# Count German holidays by year (only actual German holidays, not combined ones)
print("\nGerman holidays per year (should be 8):")
all_events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

# German holidays to look for in summaries
german_holidays = ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
                  '1. Weihnachtstag', '2. Weihnachtstag', 'Heiligabend', 'Silvester']

de_by_year = defaultdict(list)
for event in all_events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    date_match = re.search(r'DTSTART[^:]*:(\d{4})(\d{4})', event)
    
    if summary_match and date_match:
        summary = summary_match.group(1)
        year = int(date_match.group(1))
        
        # Check if this contains a German holiday name
        for holiday in german_holidays:
            if holiday in summary:
                de_by_year[year].append(holiday)
                break

for year in range(2025, 2030):
    holidays = de_by_year[year]
    unique_holidays = set(holidays)  # Remove duplicates
    status = "✅" if len(unique_holidays) == 8 else "❌"
    print(f"{year}: {len(unique_holidays)} {status}")

# Check for missing holiday names
print("\nChecking for missing holiday names:")
missing_names = 0
for event in all_events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1)
        # Check if summary has proper holiday name (not just flag + " - Closed")
        if re.search(r'^[🇺🇸🇩🇪🇬🇧\s]+ - Closed$', summary):
            missing_names += 1
            print(f"❌ Missing name: {summary}")

if missing_names == 0:
    print("✅ All events have proper holiday names")
else:
    print(f"❌ {missing_names} events missing holiday names")

# Check categories
print("\nChecking categories:")
bad_cats = content.count('ICE - UK')
if bad_cats == 0:
    print("✅ No 'ICE - UK' categories found")
else:
    print(f"❌ Found {bad_cats} instances of 'ICE - UK'")

# Check early close format
print("\nChecking early close events:")
early_close_events = [e for e in all_events if 'Early Close' in e]
datetime_count = sum(1 for e in early_close_events if 'DTSTART;TZID=' in e)
print(f"Early close events: {len(early_close_events)}")
print(f"With DATETIME format: {datetime_count}")
if len(early_close_events) == datetime_count:
    print("✅ All early close events use DATETIME")
else:
    print("❌ Some early close events still use DATE format")

# Check for SEQUENCE
sequence_count = content.count('SEQUENCE:')
print(f"\nEvents with SEQUENCE: {sequence_count}")

# Summary
print("\n" + "="*50)
issues = []

# Check actual German holiday counts
for year in range(2025, 2030):
    if len(set(de_by_year[year])) != 8:
        missing = [h for h in german_holidays if h not in de_by_year[year]]
        if missing:
            issues.append(f"{year}: Missing German holidays: {', '.join(missing)}")

if missing_names > 0:
    issues.append(f"{missing_names} events missing holiday names")
if bad_cats > 0:
    issues.append("'ICE - UK' categories still present")
if len(early_close_events) != datetime_count:
    issues.append("Early close events not all DATETIME")

if issues:
    print(f"❌ {len(issues)} issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✅ ALL CHECKS PASSED!")