# 📅 Trading Holidays Calendar 2025-2029 (v4.0.6)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Calendar Format](https://img.shields.io/badge/format-iCalendar%202.0-green.svg)
![Events](https://img.shields.io/badge/events-91-orange.svg)
![Markets](https://img.shields.io/badge/markets-NYMEX%20%7C%20CME%20%7C%20Xetra%20%7C%20ICE-red.svg)
[![GitHub Release](https://img.shields.io/github/v/release/echo-scramble/trading-holidays-ics)](https://github.com/echo-scramble/trading-holidays-ics/releases/latest)

A comprehensive iCalendar (.ics) file containing all trading holidays and early closures for US (NYMEX/CME) commodity futures, German (Xetra/Frankfurt) stock markets, and UK (ICE Futures Europe) energy markets from 2025 to 2029.

## Features

### 📅 Complete Holiday Coverage
- All official trading holidays for NYMEX/CME commodity futures
- All official trading holidays for Xetra/Frankfurt Stock Exchange
- All official trading holidays for ICE Futures Europe (Brent crude oil)
- Early closure days (US futures close at 12:00 PM CT / 1:00 PM ET)
- No weekend holidays included (markets are closed anyway, so no calendar entries needed)

### 🌍 International Compatibility
- Full timezone support (America/New_York, Europe/Berlin, and Europe/London)
- Works correctly in any timezone worldwide
- Compatible with Apple Calendar, Google Calendar, Outlook, and other calendar applications

### 🎯 Optimized Display
- Holiday names appear first for better visibility in calendar views
- Country flags (🇺🇸 🇩🇪 🇬🇧) for quick visual identification
- 🇩🇪 German market listed first in all combined events (v3.0.0)
- Combined entries for holidays affecting multiple markets
- Clear status indicators (Closed, Early Close 1PM, Geschlossen)
- Clear market type indicators (commodity futures, stock markets, energy markets)

## Calendar Format

### Holiday Title Structure
- Single market: `🇺🇸 Memorial Day - Closed`
- Combined markets: `🇩🇪🇺🇸 Karfreitag / Good Friday - Closed` (v3.0.0: DE-first)
- Early closure: `🇺🇸 Black Friday - Early Close 1PM`
- Mixed closure: `🇩🇪 Heiligabend & 🇺🇸 Christmas Eve (Early 1PM) - Mixed`

### Event Categories
- US holidays: `CATEGORIES:US,Full Day`
- US early closures: `CATEGORIES:US,Early Close`
- German holidays: `CATEGORIES:DE,Full Day`
- UK holidays: `CATEGORIES:UK,Full Day`
- Combined holidays: `CATEGORIES:DE,UK,US,Full Day` (example with all three markets)
- Mixed closures: `CATEGORIES:DE,US,Full Day,Early Close` (e.g., Christmas Eve: DE closed, US early)

## 🔔 Notifications

All events now include a built-in notification at **8:30 AM local time** on the holiday. 

### Managing Notifications in Apple Calendar

**When subscribing:**
- File → New Calendar Subscription
- After entering the URL, look for: **"Remove Alerts"**
- ✅ Toggle ON to disable all notifications
- ❌ Toggle OFF to receive 8:30 AM alerts

**On iOS/iPadOS:**
- Settings → Calendar → Accounts → Add Account → Other → Add Subscribed Calendar
- Same "Remove Alerts" option available

**Note:** Subscribed calendars are read-only. You cannot modify individual alert times.

## Quick Subscribe

📅 **Direct calendar subscription link:**
```
https://raw.githubusercontent.com/echo-scramble/trading-holidays-ics/main/Trading-Holidays-2025-2029-Combined.ics
```

🚀 **Latest Release:** [Download v4.0.6](https://github.com/echo-scramble/trading-holidays-ics/releases/latest)

## Usage

### Option 1: Subscribe to Live Updates
1. Copy the subscription link above
2. Add to your calendar app:
   - **Apple Calendar**: File → New Calendar Subscription
   - **Google Calendar**: Other calendars → From URL
   - **Outlook**: Add calendar → Subscribe from web

### Option 2: Download and Import
1. Download the [latest release](https://github.com/echo-scramble/trading-holidays-ics/releases/latest)
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

### 🇬🇧 UK Market Holidays (ICE Futures Europe)
- New Year's Day
- Good Friday
- Easter Monday
- Early May Bank Holiday
- Spring Bank Holiday
- Summer Bank Holiday
- Christmas Day
- Boxing Day

### 🇩🇪 German Market Holidays (Xetra/Frankfurt)
- Neujahr (New Year's Day)
- Karfreitag (Good Friday)
- Ostermontag (Easter Monday)
- Tag der Arbeit (Labour Day - May 1)
- Heiligabend (Christmas Eve)
- 1. Weihnachtstag (Christmas Day)
- 2. Weihnachtstag (Boxing Day)
- Silvester (New Year's Eve)

### 🇩🇪🇺🇸🇬🇧 Combined Holidays
When multiple markets are closed on the same day, entries are combined:
- Karfreitag / Good Friday (all markets)
- 1. Weihnachtstag / Christmas Day (all markets)
- Neujahr / New Year's Day (all markets)

## Technical Details

- **File Format**: iCalendar 2.0 (RFC 5545 compliant)
- **Character Encoding**: UTF-8
- **Timezone Definitions**: Includes VTIMEZONE components with DST rules
- **Event Count**: 91 events (2025-2029)
- **Transparency**: All events marked as TRANSPARENT (non-blocking)

## Data Sources

Holiday dates have been verified against:
- Official NYMEX/CME holiday announcements (2025-2027)
- Historical US federal holiday patterns (2028-2029)
- German public holiday calendar
- ICE Futures Europe Circular 24/132 (20 November 2024) for 2025
- UK bank holiday patterns for 2026-2029
- Easter date calculations for moveable holidays

### External Validation (v4.0.6)

All events have been independently verified against official sources:

- ✅ **Xetra / Börse Frankfurt** – all 8 trading holidays correctly included  
- ✅ **ICE Futures Europe** – all UK bank holidays (England & Wales) present  
- ✅ **CME / NYMEX (Energy)** – all holidays *and* early closures (1 PM ET) accounted for  
- ✅ **Weekend Policy** – no Saturday/Sunday events (91 weekday-only events)  
- ✅ **Observance Rules** – correctly shifted holidays (e.g. July 4 2026 → July 6)

#### Sources

| Market | Primary Source | Notes |
| --- | --- | --- |
| Xetra / Börse Frankfurt (DE) | [Deutsche Börse – Trading calendar & hours](https://www.xetra.com/xetra-en/Trading-calendar-and-trading-hours-22048) | Lists all DE trading holidays 2025-29 |
| ICE Futures Europe (UK) | [GOV.UK bank-holidays.json](https://www.gov.uk/bank-holidays.json) | Official UK bank-holiday data adopted by ICE |
|  | [ICE – IFEU Trading Schedule (PDF)](https://www.theice.com/publicdocs/Trading_Schedule.pdf) | Holiday hours & rare exceptions |
| CME / NYMEX (US) | [CME Group – Holiday & Trading Hours](https://www.cmegroup.com/trading-hours.html) | US energy-market holidays and 1 PM early-close rules |

## Notes

- When US holidays fall on weekends, they are observed on the closest weekday (Friday or Monday)
- German holidays that fall on weekends are excluded from this calendar
- UK holidays follow England & Wales bank holiday rules (weekend holidays move to Monday)
- Early closure information applies to regular trading hours only
- Some markets may have extended hours with different schedules

### Weekend Holiday Policy
This calendar excludes ALL holidays that naturally fall on weekends (Saturday/Sunday), regardless of market. Since trading markets are closed on weekends anyway, these entries provide no value and would only clutter the calendar. This includes:
- German holidays that don't shift (e.g., Tag der Arbeit on Saturday)
- US/UK holidays before their weekday observance shift
- Any combined holiday events falling on weekends

## Limitations

### Not Included
- **Ad-hoc early closures**: Additional early closes announced with short notice
- **Special holidays**: Unplanned events (royal occasions, national mourning)
- **Extended hours**: This calendar covers regular trading hours only

These would be added in minor releases (v4.0.x) as they are announced.

## Important Differences

### Market Differences

#### NYMEX/CME vs NYSE/NASDAQ
- NYMEX/CME observes July 2nd as early close when July 4th falls on Saturday
- Early close time is 12:00 PM CT (1:00 PM ET) for NYMEX/CME
- This calendar tracks commodity futures, not stock market holidays

#### ICE Futures Europe
- Follows UK bank holidays for England & Wales
- No early closures currently tracked (pending official circulars)
- Covers Brent crude oil and other energy futures

## License

This calendar is provided as-is for informational purposes. Please verify holiday schedules with official exchange announcements before making trading decisions.
