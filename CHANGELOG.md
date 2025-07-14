# Changelog

All notable changes to the Trading Holidays Calendar will be documented in this file.

## [4.0.6] - 2025-01-14

### Fixed
- Improved ICS file formatting for RFC 5545 compliance
- Added proper newlines between END:VEVENT and BEGIN:VEVENT blocks
- Added SEQUENCE:1 to all events (was missing from some)

### Technical Details
- Addresses formatting issue identified in external review
- Ensures stricter parsers can properly read the calendar file
- All 91 events now have consistent SEQUENCE property

## [4.0.5] - 2025-01-14

### Changed
- **REMOVED** all weekend holiday entries (6 events removed)
- Total events decreased from 97 to 91
- Updated README with explicit weekend holiday policy
- Added comprehensive weekend handling documentation

### Removed
- 🇩🇪 Tag der Arbeit (May 1, 2027 - Saturday)
- 🇩🇪 1. Weihnachtstag (Dec 25, 2027 - Saturday)  
- 🇩🇪 2. Weihnachtstag (Dec 26, 2027 - Sunday)
- 🇩🇪 Neujahr (Jan 1, 2028 - Saturday)
- 🇩🇪🇺🇸 Heiligabend / Christmas Eve (Dec 24, 2028 - Sunday)
- 🇩🇪 Silvester (Dec 31, 2028 - Sunday)

### Rationale
Markets are closed on weekends regardless of holidays. Weekend entries provide no trading value and only clutter the calendar.

## [4.0.4] - 2025-01-13

### Fixed
- Updated PRODID to v4.0.4 to match release version
- Removed '-mixed' suffix from UIDs (was: `20251224-de-us-mixed@`, now: `20251224-de-us@`)
- Verified all 97 events have flag emojis in SUMMARY lines

### Technical Details
- All UIDs now follow consistent pattern: `{date}-{countries}@trading-holidays.com`
- PRODID properly incremented for each release
- No more legacy suffixes in identifiers

## [4.0.3] - 2025-01-13

### Fixed
- Updated PRODID to v4.0.3 (was incorrectly showing v4.0.1 in v4.0.2)
- Standardized all UK UIDs from 'ice-uk' to 'uk' for consistency
- Replaced 'Mixed' category with 'Full Day,Early Close' for combined events
- Ensured all flag emojis are present in SUMMARY lines

## [4.0.2] - 2025-01-13

### Changed
- **REMOVED** Tag der Deutschen Einheit (Oct 3, 2027) - Not a stock exchange holiday
- Converted Early Close events to All-Day format (VALUE=DATE) for better calendar integration
- Combined Dec 24 events: Single entry showing "DE Closed, US Early Close 1PM"
- Updated PRODID to v4.0.1 for proper versioning
- Total events decreased from 102 to 97

### Fixed  
- Added missing flag emojis (🇩🇪🇬🇧🇺🇸) to all event summaries
- Corrected VALARM text for Early Close events: "Markets close early at 1:00 PM ET"
- Eliminated duplicate calendar entries for days with mixed closures

## [4.0.1] - 2025-01-13

### Fixed
- Added missing Tag der Deutschen Einheit (Oct 3, 2027)  
- Standardized status indicators: "Geschlossen" → "Closed"
- Fixed "Early Close" → "Early Close 1PM" for consistency
- Corrected misleading summaries (Christmas Eve/New Year's Eve)
- Added missing VALARM blocks to Christmas Eve early close events
- Total events increased from 101 to 102

## [4.0.0] - 2025-07-13
- Added: ICE Futures Europe (UK) market support integrated with existing events
- Added: Europe/London timezone definition for BST/GMT transitions
- Added: UK market to combined events (Good Friday, Christmas, etc.)
- Added: 13 unique UK-only events (Early May and Summer Bank Holidays)
- Changed: Total event count increased from 78 to 101
- Changed: Updated combined events to show 🇩🇪🇺🇸🇬🇧 or 🇩🇪🇬🇧 or 🇺🇸🇬🇧
- Changed: Categories now include `ICE - UK` in combined events
- Fixed: Properly combined overlapping holidays instead of duplicating
- Note: ICE 2025 holidays based on official Circular 24/132 (20 November 2024)
- Note: ICE 2026-2029 holidays calculated based on UK bank holiday patterns

## [3.5.1] - 2025-07-13
- Fixed: Notifications now correctly trigger at 8:30 AM on event day (was: day before)

## [3.5.0] - 2025-07-13
- Added: Built-in notifications at 8:30 AM local time for all events
- Added: Instructions for managing notifications in Apple Calendar

## [3.0.0] - 2025-07-13
- Changed: DE-first ordering for all mixed market events (breaking change)
- Changed: CATEGORIES order from US,DE to DE,US
- Changed: Flag order in titles to show 🇩🇪🇺🇸
- Changed: Description fields now list German markets first

## [2.0.0] - 2025-07-13
- Initial public release
- Combined US (NYMEX/CME) and German (Xetra/Frankfurt) trading holidays
- 78 events covering 2025-2029
- Full timezone support