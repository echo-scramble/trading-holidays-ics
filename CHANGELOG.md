# Changelog

All notable changes to the Trading Holidays Calendar will be documented in this file.

## [4.0.0] - 2025-07-13
- Added: ICE Futures Europe (UK) market support integrated with existing events
- Added: Europe/London timezone definition for BST/GMT transitions
- Added: UK market to combined events (Good Friday, Christmas, etc.)
- Added: 13 unique UK-only events (Early May and Summer Bank Holidays)
- Changed: Total event count increased from 78 to 91
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