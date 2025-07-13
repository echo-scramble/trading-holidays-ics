#!/usr/bin/env python3

import re
from collections import defaultdict

# Read the final file
with open('Trading-Holidays-2025-2029-Combined-FINAL.ics', 'r') as f:
    content = f.read()

# Extract all events
events = re.findall(r'BEGIN:VEVENT.*?END:VEVENT', content, re.DOTALL)

print(f"Total events: {len(events)}\n")

# Check categories
print("Checking categories...")
bad_categories = []
for event in events:
    cat_match = re.search(r'CATEGORIES:(.*)', event)
    if cat_match:
        categories = cat_match.group(1)
        if 'ICE - UK' in categories:
            bad_categories.append(categories)

if bad_categories:
    print(f"❌ Found {len(bad_categories)} events with 'ICE - UK'")
else:
    print("✅ All categories fixed (no 'ICE - UK')")

# Check for flags in summaries
print("\nChecking flags in summaries...")
no_flag_count = 0
for event in events:
    summary_match = re.search(r'SUMMARY:(.*)', event)
    if summary_match:
        summary = summary_match.group(1)
        if not any(flag in summary for flag in ['🇺🇸', '🇩🇪', '🇬🇧']):
            no_flag_count += 1

if no_flag_count > 0:
    print(f"❌ Found {no_flag_count} events without flags")
else:
    print("✅ All events have flags")

# Check German holidays per year
print("\nGerman holidays per year:")
de_by_year = defaultdict(int)
for event in events:
    if 'CATEGORIES:DE' in event or ',DE,' in event or event.endswith(',DE,Full Day\n'):
        date_match = re.search(r'DTSTART[^:]*:(\d{4})(\d{4})', event)
        if date_match:
            year = int(date_match.group(1))
            de_by_year[year] += 1

for year in sorted(de_by_year.keys()):
    status = "✅" if de_by_year[year] == 8 else "❌"
    print(f"{year}: {de_by_year[year]} {status}")

# Check for early close datetime
print("\nChecking early close events...")
early_close_count = 0
early_close_datetime = 0
for event in events:
    if 'Early Close' in event:
        early_close_count += 1
        if 'DTSTART;TZID=' in event:
            early_close_datetime += 1

print(f"Early close events: {early_close_count}")
print(f"With DATETIME format: {early_close_datetime}")
if early_close_count == early_close_datetime:
    print("✅ All early close events use DATETIME")
else:
    print("❌ Some early close events still use DATE")

# Check for duplicates
print("\nChecking for duplicate dates...")
dates = []
for event in events:
    date_match = re.search(r'DTSTART[^:]*:(\d{8})', event)
    if date_match:
        dates.append(date_match.group(1))

date_counts = defaultdict(int)
for date in dates:
    date_counts[date] += 1

duplicates = [(d, c) for d, c in date_counts.items() if c > 1]
if duplicates:
    print(f"❌ Found {len(duplicates)} duplicate dates:")
    for date, count in sorted(duplicates):
        print(f"  {date}: {count} events")
else:
    print("✅ No duplicate dates")

# Check metadata
print("\nChecking metadata...")
if 'PRODID:-//Trading Holidays//Calendar v4.0.0//EN' in content:
    print("✅ PRODID updated to v4.0.0")
else:
    print("❌ PRODID not updated")

if 'UK (ICE Futures Europe)' in content:
    print("✅ Description includes UK markets")
else:
    print("❌ Description missing UK markets")

if 'X-WR-TIMEZONE:America/New_York' in content:
    print("⚠️  X-WR-TIMEZONE still set to America/New_York (should be removed)")
else:
    print("✅ X-WR-TIMEZONE removed or set to UTC")

# Check SEQUENCE numbers
print("\nChecking SEQUENCE numbers...")
sequence_count = content.count('SEQUENCE:')
print(f"Events with SEQUENCE: {sequence_count}")

# Summary
print("\n" + "="*50)
print("VALIDATION SUMMARY")
print("="*50)

issues = []
if bad_categories:
    issues.append("Fix 'ICE - UK' categories")
if no_flag_count > 0:
    issues.append(f"Add flags to {no_flag_count} events")
if any(de_by_year[y] != 8 for y in de_by_year):
    issues.append("Fix German holiday counts")
if early_close_count != early_close_datetime:
    issues.append("Convert remaining early close to DATETIME")
if duplicates:
    issues.append("Remove duplicate dates")
if 'PRODID:-//Trading Holidays//Calendar v4.0.0//EN' not in content:
    issues.append("Update PRODID")
if 'X-WR-TIMEZONE:America/New_York' in content:
    issues.append("Remove X-WR-TIMEZONE")

if issues:
    print(f"\n❌ {len(issues)} issues to fix:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n✅ ALL VALIDATIONS PASSED!")