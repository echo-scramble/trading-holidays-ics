#!/usr/bin/env python3

import re
from collections import defaultdict

# Read the file
with open('Trading-Holidays-2025-2029-Combined.ics', 'r') as f:
    content = f.read()

print("# Final Validation Report for v4.0.2\n")

# Count events
events = re.findall(r'BEGIN:VEVENT', content)
print(f"Total events: {len(events)}")

# Check header
if 'PRODID:-//Trading Holidays//Calendar v4.0.1//EN' in content:
    print("✅ PRODID: v4.0.1")
else:
    print("❌ PRODID not updated to v4.0.1")

if 'UK (ICE Futures Europe)' in content:
    print("✅ Description includes UK")
else:
    print("❌ Description missing UK")

# Count German holidays by year
print("\nGerman holidays per year (should be 8):")
all_events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

german_holidays = ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
                  '1. Weihnachtstag', '2. Weihnachtstag', 'Heiligabend', 'Silvester']

de_by_year = defaultdict(list)
for event in all_events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    date_match = re.search(r'DTSTART[^:]*:(\d{4})(\d{4})', event)
    
    if summary_match and date_match:
        summary = summary_match.group(1)
        year = int(date_match.group(1))
        
        for holiday in german_holidays:
            if holiday in summary:
                de_by_year[year].append(holiday)
                break

for year in range(2025, 2030):
    holidays = de_by_year[year]
    unique_holidays = set(holidays)
    status = "✅" if len(unique_holidays) == 8 else "❌"
    print(f"{year}: {len(unique_holidays)} {status}")

# Check for missing holiday names
print("\nChecking for missing holiday names:")
missing_names = 0
for event in all_events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1)
        # Check for empty holiday names
        if re.search(r'^[🇺🇸🇩🇪🇬🇧\s]+ - (Closed|Early Close)$', summary):
            missing_names += 1
            print(f"❌ Missing name: {summary}")

if missing_names == 0:
    print("✅ All events have proper holiday names")

# Check for flag emojis
print("\nChecking for flag emojis:")
no_flag_count = 0
for event in all_events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1)
        if not any(flag in summary for flag in ['🇺🇸', '🇩🇪', '🇬🇧']):
            no_flag_count += 1
            print(f"❌ No flag: {summary}")

if no_flag_count == 0:
    print("✅ All events have flag emojis")
else:
    print(f"❌ {no_flag_count} events missing flags")

# Check categories
print("\nChecking categories:")
bad_cats = content.count('ICE - UK')
if bad_cats == 0:
    print("✅ No 'ICE - UK' categories found")
else:
    print(f"❌ Found {bad_cats} instances of 'ICE - UK'")

# Check early close format - should be VALUE=DATE now
print("\nChecking early close events (should use VALUE=DATE):")
early_close_events = [e for e in all_events if 'Early Close' in e]
date_format_count = sum(1 for e in early_close_events if 'DTSTART;VALUE=DATE' in e)
print(f"Early close events: {len(early_close_events)}")
print(f"With VALUE=DATE format: {date_format_count}")
if len(early_close_events) == date_format_count:
    print("✅ All early close events use VALUE=DATE")
else:
    print("❌ Some early close events don't use VALUE=DATE")

# Check VALARM text for early close
print("\nChecking VALARM text for early close events:")
wrong_valarm = 0
for event in early_close_events:
    if 'Markets closed today' in event:
        wrong_valarm += 1

if wrong_valarm == 0:
    print("✅ All early close VALARM texts are correct")
else:
    print(f"❌ {wrong_valarm} early close events have wrong VALARM text")

# Check for combined Dec 24 events
print("\nChecking Dec 24 combined events:")
dec24_count = sum(1 for e in all_events if '1224' in e and 'DE Closed, US Early Close' in e)
print(f"Combined Dec 24 events: {dec24_count} (should be 4)")

# Check for Tag der Deutschen Einheit
print("\nChecking Tag der Deutschen Einheit (should be removed):")
tde_count = content.count('Tag der Deutschen Einheit') + content.count('20271003')
if tde_count == 0:
    print("✅ Tag der Deutschen Einheit correctly removed")
else:
    print(f"❌ Tag der Deutschen Einheit still present ({tde_count} references)")

# Summary
print("\n" + "="*50)
print("VALIDATION SUMMARY")
print("="*50)

issues = []
if 'PRODID:-//Trading Holidays//Calendar v4.0.1//EN' not in content:
    issues.append("PRODID not updated to v4.0.1")
if no_flag_count > 0:
    issues.append(f"{no_flag_count} events missing flag emojis")
if len(early_close_events) != date_format_count:
    issues.append("Early close events not all VALUE=DATE")
if wrong_valarm > 0:
    issues.append("Some early close events have wrong VALARM text")
if tde_count > 0:
    issues.append("Tag der Deutschen Einheit not removed")

if issues:
    print(f"\n❌ {len(issues)} issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n✅ ALL VALIDATIONS PASSED!")