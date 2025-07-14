# Implementation Notes for Trading Holiday Calendars (NYMEX/CME, Xetra, ICE Focus)

## Version History

### v4.0.5 (2025-01-14)
- **Policy Change**: Removed all weekend holiday entries
- Removed 6 events that fall on Saturday/Sunday
- Total events decreased from 97 to 91
- Updated README with explicit weekend holiday policy
- Rationale: Markets closed on weekends anyway, entries provide no value

### v4.0.0 (2025-07-13)
- **Major Feature**: Added ICE Futures Europe (UK) market support
- Properly integrated UK holidays with existing US/DE events
- Added 13 unique UK-only events (Early May and Summer Bank Holidays)
- Added Europe/London timezone definition
- Combined overlapping holidays (Good Friday, Christmas, Memorial Day/Spring Bank, etc.)
- Total events increased from 78 to 101 (not 118 - avoiding duplicates)
- Data source: ICE Circular 24/132 (20 November 2024) for 2025

### v3.5.1 (2025-07-13)
- **Bug Fix**: Corrected notification timing to 8:30 AM on event day
- Changed TRIGGER from `-PT15H30M` to `PT8H30M`
- Previous version incorrectly notified day before event

### v3.5.0 (2025-07-13)
- **New Feature**: Added VALARM components to all 78 events
- Notifications at 8:30 AM local time on trading holidays
- Users can disable via "Remove Alerts" option when subscribing
- File size increased from 23KB to 32KB

### v3.0.0 (2025-07-13)
- **Major Change**: DE-first ordering for all mixed market events
- Changed CATEGORIES order from `US,DE` to `DE,US` for all combined events
- Updated flag order in SUMMARY to consistently show 🇩🇪 first
- Mixed events now display: "🇩🇪 Heiligabend & 🇺🇸 Christmas Eve (Early 1PM)"
- Reflects primary German market audience and European market priority
- Breaking change for systems parsing exact CATEGORIES format

### v2.0.0 (Initial Release)
- Combined US commodity futures and German stock market holidays
- 5-year calendar (2025-2029)
- Comprehensive holiday coverage with early closures

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

### 1a. UK/ICE Market Holidays - Bank Holidays for England & Wales
**IMPORTANT**: Only these 8 days are ICE Futures Europe holidays:
- New Year's Day, Good Friday, Easter Monday, Early May Bank Holiday,
- Spring Bank Holiday, Summer Bank Holiday, Christmas Day, Boxing Day

**NOT market holidays** (Northern Ireland/Scotland specific):
- ❌ St Patrick's Day (March 17 - Northern Ireland)
- ❌ 2nd January (Scotland only)
- ❌ St Andrew's Day (November 30 - Scotland)
- ❌ July 12 (Northern Ireland only)

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
SUMMARY:🇩🇪 Holiday Name - Status      # Flag + Space + Name + Status (DE-first for mixed)
DESCRIPTION:Clear description         # What's closed/when
CATEGORIES:XX,Status                  # DE/US/both + Full Day/Early Close/Mixed (DE-first)
TRANSP:TRANSPARENT                    # Non-blocking in calendars
BEGIN:VALARM                          # Notification component (v3.5.0+)
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M                       # 8:30 AM on event day (8.5 hours after midnight)
END:VALARM
END:VEVENT
```

### 6. Category System
- `US,Full Day`: US commodity futures markets closed all day
- `US,Early Close`: US commodity futures markets close at 12 PM CT / 1 PM ET
- `DE,Full Day`: German stock markets closed all day
- `UK,Full Day`: ICE Futures Europe (Brent) closed all day
- `DE,UK,US,Full Day`: All three markets closed all day
- `DE,US,Full Day,Early Close`: Different closure types (e.g., DE full, US early)

### 7. Timezone Handling
- All-day events use `VALUE=DATE` (no timezone needed)
- Include VTIMEZONE definitions for America/New_York, Europe/Berlin, and Europe/London
- Early close times should reference both CT and ET in description
- UK timezone uses Europe/London (handles BST/GMT transitions)

### 8. Notification Implementation (v3.5.0+)
- **VALARM Component**: Added to all 78 events
- **Trigger Time**: `PT8H30M` = 8.5 hours after event start (00:00)
- **Local Time**: Notifications appear at 8:30 AM in user's timezone
- **User Control**: Can be disabled via "Remove Alerts" in calendar apps
- **Compatibility**: Works with Apple Calendar, Google Calendar, Outlook
- **Important**: Do NOT use negative trigger (e.g., `-PT15H30M`) as it calculates from day before

### 9. Weekend Holiday Policy (v4.0.5+)
**STRICT RULE**: NO weekend entries in the calendar, regardless of market.

**Rationale**: Markets are closed on weekends anyway, so weekend holiday entries:
- Provide no trading value
- Clutter the calendar unnecessarily
- May confuse users about actual trading days

**What gets excluded**:
- German holidays that naturally fall on weekends (they don't shift)
- US/UK holidays BEFORE their observance shift is applied
- Any combined events falling on weekends

**Examples of excluded entries**:
- Tag der Arbeit when May 1 falls on Saturday
- Heiligabend when Dec 24 falls on Sunday (even with US early close)
- 1. Weihnachtstag when Dec 25 falls on Saturday

**What gets included**:
- The shifted observance dates (e.g., Monday for Sunday holidays)
- All holidays falling Monday-Friday

### 10. Data Validation Checklist
Before release, verify:
1. Total event count matches documentation
2. **NO events on weekends** (critical for v4.0.5+)
3. No duplicate events on same date (check thoroughly - same date should appear only once)
4. All German holidays are in the official 8-holiday list
5. US observance rules correctly applied
6. Easter-based holidays calculated correctly
7. July 3rd early close when July 4th falls on weekday; July 2nd early close when July 4th falls on Saturday (NYMEX/CME specific)
8. Consistent handling of "mixed" closure days (e.g., Christmas Eve)

### 11. Easter Calculation
Easter moves each year. Key dates:
- Good Friday: 2 days before Easter
- Easter Monday: 1 day after Easter
- Ascension Day: 39 days after Easter (NOT a market holiday!)
- Whit Monday: 50 days after Easter (NOT a market holiday!)

### 12. NYMEX/CME Specific Rules
- July 2nd is an early close when July 4th falls on Saturday (differs from NYSE)
- Early close is at 12:00 PM CT (Central Time) / 1:00 PM ET
- Commodity futures markets may have different holiday rules than equity markets

### 13. Mixed Market Types
- This calendar combines commodity futures (US), stock markets (German), and energy futures (UK)
- Always specify market type in descriptions to avoid confusion
- US: "commodity futures markets"
- DE: "stock markets"
- UK: "ICE Futures Europe (Brent)"

### 14. Testing Commands
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
- ICE Futures Europe: ICE Circulars (e.g., Circular 24/132 for 2025)
- Easter dates: astronomical calculations or established tables
- Federal holidays: Vary by year due to observance rules
- UK bank holidays: gov.uk/bank-holidays (England & Wales only)

## Additional Notes
1. **Never trust Wikipedia** for market holidays - use official exchange sources
2. **German regional holidays** (like Bavarian holidays) do NOT affect Xetra
3. **Early closures** exist only in US markets (12 PM CT), not German
4. **Good Friday** is the only holiday that always aligns in both markets
5. **May 1st** can fall on weekends - exclude if so (Labor Day vs Tag der Arbeit confusion)