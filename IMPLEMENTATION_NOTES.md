# Implementation Notes for Trading Holiday Calendars (NYMEX/CME Focus)

## Critical Rules Not Obvious from README

### 1. German Market Holidays - Common Misconceptions
**IMPORTANT**: Only these 8 days are Xetra/Frankfurt market holidays:
- Neujahr, Karfreitag, Ostermontag, Tag der Arbeit (May 1), Heiligabend, 1. & 2. Weihnachtstag, Silvester

**NOT market holidays** (markets are OPEN):
- ❌ Christi Himmelfahrt (Ascension Day)
- ❌ Pfingstmontag (Whit Monday)
- ❌ Tag der Deutschen Einheit (Oct 3)
- ❌ Fronleichnam (Corpus Christi)
- ❌ Reformationstag (Reformation Day)
- ❌ Allerheiligen (All Saints' Day)

### 2. US Holiday Observance Rules (NYMEX/CME)
When holidays fall on weekends:
- **Saturday → Friday**: Holiday observed on preceding Friday
- **Sunday → Monday**: Holiday observed on following Monday
- **Exception**: Good Friday is always on Friday (no observance needed)

### 3. Christmas Eve Special Rules
- **Normal years**: US early close (12 PM CT / 1 PM ET), DE fully closed → "Mixed" event
- **When Dec 25 = Saturday**: US observes on Dec 24 (full closure) → Combined full closure
- **When Dec 25 = Sunday**: US observes on Dec 26 (Monday), Dec 24 has only DE closure

### 4. Event Combination Logic
Combine events when both markets are closed **all day** on the same date:
- ✅ Good Friday (both closed)
- ✅ Christmas Day (both closed, when on weekday)
- ✅ New Year's Day (both closed, when on weekday)

Do NOT combine when closure types differ:
- ❌ Christmas Eve (usually US early, DE full)
- ❌ Any US early close day

### 5. ICS Format Requirements
```
BEGIN:VEVENT
DTSTART;VALUE=DATE:YYYYMMDD           # All-day event format
DTSTAMP:YYYYMMDDTHHMMSSZ              # Timestamp when created
UID:YYYYMMDD-xx-xx@trading-holidays.com  # Unique ID
SUMMARY:🇺🇸 Holiday Name - Status      # Flag + Space + Name + Status
DESCRIPTION:Clear description         # What's closed/when
CATEGORIES:XX,Status                  # US/DE/both + Full Day/Early Close/Mixed
TRANSP:TRANSPARENT                    # Non-blocking in calendars
END:VEVENT
```

### 6. Category System
- `US,Full Day`: US commodity futures markets closed all day
- `US,Early Close`: US commodity futures markets close at 12 PM CT / 1 PM ET
- `DE,Full Day`: German stock markets closed all day
- `US,DE,Full Day`: US futures and German stock markets closed all day
- `US,DE,Mixed`: Different closure types (e.g., US early, DE full)

### 7. Timezone Handling
- All-day events use `VALUE=DATE` (no timezone needed)
- Include VTIMEZONE definitions for both America/New_York and Europe/Berlin
- Early close times should reference both CT and ET in description

### 8. Data Validation Checklist
Before release, verify:
1. Total event count matches documentation
2. No events on weekends (use `date -d YYYYMMDD` to check)
3. No duplicate events on same date (check thoroughly - same date should appear only once)
4. All German holidays are in the official 8-holiday list
5. US observance rules correctly applied
6. Easter-based holidays calculated correctly
7. July 3rd early close when July 4th falls on weekday; July 2nd early close when July 4th falls on Saturday (NYMEX/CME specific)
8. Consistent handling of "mixed" closure days (e.g., Christmas Eve)

### 9. Easter Calculation
Easter moves each year. Key dates:
- Good Friday: 2 days before Easter
- Easter Monday: 1 day after Easter
- Ascension Day: 39 days after Easter (NOT a market holiday!)
- Whit Monday: 50 days after Easter (NOT a market holiday!)

### 10. NYMEX/CME Specific Rules
- July 2nd is an early close when July 4th falls on Saturday (differs from NYSE)
- Early close is at 12:00 PM CT (Central Time) / 1:00 PM ET
- Commodity futures markets may have different holiday rules than equity markets

### 11. Mixed Market Types
- This calendar combines commodity futures (US) with stock markets (German)
- Always specify market type in descriptions to avoid confusion
- US: "commodity futures markets"
- DE: "stock markets"

### 12. Testing Commands
```bash
# Count events
grep -c "BEGIN:VEVENT" calendar.ics

# Find duplicates
grep "DTSTART;VALUE=DATE:" calendar.ics | sort | uniq -d

# Check for weekend dates
while read date; do
  d=$(echo $date | grep -o '[0-9]\{8\}')
  echo "$d: $(date -d "${d:0:4}-${d:4:2}-${d:6:2}" +%A)"
done < <(grep "DTSTART;VALUE=DATE:" calendar.ics)

# Verify no forbidden German holidays
grep -E "(Himmelfahrt|Pfingstmontag|Deutschen Einheit)" calendar.ics
```

## Common Pitfalls
1. **Line folding**: Ensure each event is on separate lines, not folded
2. **Automated holiday APIs**: Often include regional holidays not relevant for markets
3. **German public holidays**: Most are NOT market holidays
4. **Christmas week**: Complex rules when holidays fall on weekends
5. **Event counting**: Simple grep works only if properly formatted

## Sources for Verification
- NYMEX/CME: Official CME Group holiday calendar
- Xetra: deutsche-boerse.com trading calendar (only 8 holidays per year!)
- Easter dates: astronomical calculations or established tables
- Federal holidays: Vary by year due to observance rules

## Additional Notes
1. **Never trust Wikipedia** for market holidays - use official exchange sources
2. **German regional holidays** (like Bavarian holidays) do NOT affect Xetra
3. **Early closures** exist only in US markets (12 PM CT), not German
4. **Good Friday** is the only holiday that always aligns in both markets
5. **May 1st** can fall on weekends - exclude if so (Labor Day vs Tag der Arbeit confusion)