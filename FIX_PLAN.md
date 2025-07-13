# 🔧 Gesamtplan zur Korrektur der Trading Holidays Calendar v4.0.0

## A. Inhaltliche Korrekturen (aus Prüfbericht)

### 1. Fehlende DE Feiertage ergänzen
- **2026**: 2. Weihnachtstag (26.12.) als DE+UK kombinieren
- **2027**: Tag der Arbeit (1.5.) für DE hinzufügen
- **2027**: 2. Weihnachtstag korrekt als DE+UK
- **2027**: Silvester nur als DE (nicht US+DE)
- **2028**: Silvester (31.12.) für DE hinzufügen

### 2. Doppelte Events kombinieren
- **2025-01-01**: US und UK zu einem 🇺🇸🇬🇧 Event vereinen

### 3. Kombinationen korrigieren
- Events die am selben Tag in mehreren Märkten sind, richtig kombinieren

## B. Technische Korrekturen (aus Nachtrag)

### 1. Metadaten (Header)
- PRODID: Version auf v4.0.0 ändern
- X-WR-CALDESC: UK Märkte erwähnen
- X-WR-TIMEZONE: Entfernen oder auf UTC setzen

### 2. Kategorie-Schema
- "ICE - UK" → "UK" (ohne Leerzeichen)
- Reihenfolge standardisieren: DE, UK, US (alphabetisch/geografisch)
- "Mixed" dokumentieren oder eliminieren

### 3. SUMMARY Format
- Flags wiederherstellen für alle Märkte
- Format: `🇩🇪🇬🇧🇺🇸 Karfreitag / Good Friday - Closed`

### 4. Early Close Events
- Von DATE zu DATETIME konvertieren
- Beispiel: `DTSTART;TZID=America/New_York:20250703T130000`
- DTEND hinzufügen für Zeitspanne

### 5. DTSTAMP
- Individualisieren mit aktuellem Timestamp beim Generieren

## C. Implementierungsreihenfolge

### Phase 1: Datenkorrektur-Script
1. Alle Events einlesen und parsen
2. Fehlende DE Feiertage ergänzen
3. Doppelte Events identifizieren und kombinieren
4. Kategorie-Schema korrigieren (ICE - UK → UK)
5. Mixed Events aufteilen oder dokumentieren

### Phase 2: Format-Korrektur
1. Header/Metadaten aktualisieren
2. SUMMARY mit Flags neu generieren
3. Early Close Events zu DATETIME konvertieren
4. DTSTAMP individualisieren

### Phase 3: Validierung
1. Event-Zählung prüfen (sollte ~86-88 Events sein)
2. DE Feiertage: 8 pro Jahr verifizieren
3. Keine Duplikate
4. Kategorie-Konsistenz prüfen

## D. Erwartete Änderungen

### Events vorher/nachher
- Vorher: 101 Events
- Nachher: ~86-88 Events (durch Kombinierung)

### Neue Event-Struktur Beispiel
```ics
BEGIN:VEVENT
DTSTART;VALUE=DATE:20250418
DTEND;VALUE=DATE:20250419
DTSTAMP:20250713T143022Z
UID:20250418-de-uk-us-closed@trading-holidays.com
SUMMARY:🇩🇪🇬🇧🇺🇸 Karfreitag / Good Friday - Closed
DESCRIPTION:German stock markets, ICE Futures Europe (Brent) and US commodity futures markets closed all day
CATEGORIES:DE,UK,US,Full Day
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:⚠️ Trading Holiday: Markets closed today
TRIGGER:PT8H30M
END:VALARM
END:VEVENT
```

### Early Close Beispiel
```ics
BEGIN:VEVENT
DTSTART;TZID=America/New_York:20250703T093000
DTEND;TZID=America/New_York:20250703T130000
DTSTAMP:20250713T143023Z
UID:20250703-us-early@trading-holidays.com
SUMMARY:🇺🇸 Independence Day Eve - Early Close
DESCRIPTION:US commodity futures markets close at 12:00 PM CT / 1:00 PM ET
CATEGORIES:US,Early Close
TRANSP:TRANSPARENT
END:VEVENT
```

## E. Qualitätssicherung

1. **ICS Validator** durchlaufen lassen
2. **Import-Test** in Apple Calendar, Google Calendar, Outlook
3. **Filter-Test**: "Zeige nur UK" muss funktionieren
4. **Mobile Test**: Flags müssen sichtbar sein
5. **Sync-Test**: Änderungen müssen erkannt werden