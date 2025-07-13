# Release Notes v3.5.0

## 🔔 What's New

### Built-in Notifications
- All 78 events now include an alert at **8:30 AM local time** on the holiday
- Works in any timezone - always 8:30 AM in YOUR local time
- Helps traders remember market closures before the trading day begins

### User Control
- Notifications can be disabled when subscribing:
  - Apple Calendar: Toggle "Remove Alerts" when adding subscription
  - Other apps: Check notification settings
- Existing subscribers: Re-subscribe or update settings to manage alerts

## 📱 How to Manage Notifications

### Apple Calendar (macOS)
1. File → New Calendar Subscription
2. Enter the URL
3. **"Remove Alerts"** - Toggle ON to disable notifications

### Apple Calendar (iOS/iPadOS)
1. Settings → Calendar → Accounts
2. Add Account → Other → Add Subscribed Calendar
3. Same "Remove Alerts" option available

### Other Calendar Apps
- Google Calendar: Notifications settings in calendar properties
- Outlook: Alert options when subscribing

## 🔧 Technical Details
- Alert trigger: `-PT15H30M` (15.5 hours before event = 8:30 AM)
- Alert type: `DISPLAY` with description
- Works with all-day events across timezones

## 📌 No Breaking Changes
- Same subscription URL
- Calendar structure unchanged
- Only addition is VALARM components

## 🎯 Why 8:30 AM?
- Before market open in all major timezones
- Sufficient time to adjust trading plans
- Not too early to be disruptive