# Trading Holidays Calendar 2025-2029

A comprehensive iCalendar (.ics) file containing all trading holidays and early closures for US (NYMEX/CME) commodity futures and German (Xetra/Frankfurt) stock markets from 2025 to 2029.

## Features

### 📅 Complete Holiday Coverage
- All official trading holidays for NYMEX/CME commodity futures
- All official trading holidays for Xetra/Frankfurt Stock Exchange
- Early closure days (US futures close at 12:00 PM CT / 1:00 PM ET)
- No weekend holidays included (markets are closed anyway)

### 🌍 International Compatibility
- Full timezone support (America/New_York and Europe/Berlin)
- Works correctly in any timezone worldwide
- Compatible with Apple Calendar, Google Calendar, Outlook, and other calendar applications

### 🎯 Optimized Display
- Holiday names appear first for better visibility in calendar views
- Country flags (🇺🇸 🇩🇪) for quick visual identification
- Combined entries for holidays affecting both markets
- Clear status indicators (Closed, Early Close 1PM, Geschlossen)
- Clear market type indicators (commodity futures vs. stock markets)

## Calendar Format

### Holiday Title Structure
- Single market: `🇺🇸 Memorial Day - Closed`
- Combined markets: `🇺🇸🇩🇪 Good Friday / Karfreitag - Closed`
- Early closure: `🇺🇸 Black Friday - Early Close 1PM`

### Event Categories
- US holidays: `CATEGORIES:US,Full Day`
- US early closures: `CATEGORIES:US,Early Close`
- German holidays: `CATEGORIES:DE,Full Day`
- Combined holidays: `CATEGORIES:US,DE,Full Day`
- Mixed closures: `CATEGORIES:US,DE,Mixed` (e.g., Christmas Eve: US early, DE closed)

## Usage

1. Download the `Trading-Holidays-2025-2029-Combined.ics` file
2. Import into your calendar application:
   - **Apple Calendar**: Double-click the file or File → Import
   - **Google Calendar**: Settings → Import & Export → Import
   - **Outlook**: File → Open & Export → Import/Export

## Holiday Details

### 🇺🇸 US Market Holidays (NYMEX/CME)
- New Year's Day
- Martin Luther King Jr. Day
- Presidents' Day
- Good Friday
- Memorial Day
- Juneteenth
- Independence Day
- Labor Day
- Thanksgiving Day
- Christmas Day

### 🇺🇸 US Early Closures (12:00 PM CT / 1:00 PM ET)
- Day before Independence Day
- Black Friday (day after Thanksgiving)
- Christmas Eve (only when Christmas falls on a weekday; if Christmas falls on Saturday, Dec 24 is a full holiday)
- July 2nd when Independence Day falls on Saturday (NYMEX/CME specific)

### 🇩🇪 German Market Holidays (Xetra/Frankfurt)
- Neujahr (New Year's Day)
- Karfreitag (Good Friday)
- Ostermontag (Easter Monday)
- Tag der Arbeit (Labour Day - May 1)
- Heiligabend (Christmas Eve)
- 1. Weihnachtstag (Christmas Day)
- 2. Weihnachtstag (Boxing Day)
- Silvester (New Year's Eve)

### 🇺🇸🇩🇪 Combined Holidays
When both markets are closed on the same day, entries are combined:
- Good Friday / Karfreitag
- Christmas Day / 1. Weihnachtstag
- New Year's Day / Neujahr

## Technical Details

- **File Format**: iCalendar 2.0 (RFC 5545 compliant)
- **Character Encoding**: UTF-8
- **Timezone Definitions**: Includes VTIMEZONE components with DST rules
- **Event Count**: 78 events (2025-2029)
- **Transparency**: All events marked as TRANSPARENT (non-blocking)

## Data Sources

Holiday dates have been verified against:
- Official NYMEX/CME holiday announcements (2025-2027)
- Historical US federal holiday patterns (2028-2029)
- German public holiday calendar
- Easter date calculations for moveable holidays

## Notes

- When US holidays fall on weekends, they are observed on the closest weekday (Friday or Monday)
- German holidays that fall on weekends are excluded
- Early closure information applies to regular trading hours only
- Some markets may have extended hours with different schedules

## Important Differences

### NYMEX/CME vs NYSE/NASDAQ
- NYMEX/CME observes July 2nd as early close when July 4th falls on Saturday
- Early close time is 12:00 PM CT (1:00 PM ET) for NYMEX/CME
- This calendar tracks commodity futures, not stock market holidays

## License

This calendar is provided as-is for informational purposes. Please verify holiday schedules with official exchange announcements before making trading decisions.
