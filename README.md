# 🗺️ INTERLIS1 WebGIS Professional

Ein interaktives WebGIS-Tool zur Visualisierung und Analyse von Schweizer Vermessungsdaten direkt im Browser - ohne Installation, ohne Server.


## 🚀 Features

- **📁 Drag & Drop**: GeoJSON-Dateien einfach laden
- **🔍 Intelligente Suche**: Durchsucht alle Feature-Attribute
- **📊 Attribut-Tabelle**: Sortierbar mit CSV-Export
- **🎨 Style-Editor**: Individuelle Farben, Grössen & Symbole pro Layer
- **💾 Export-Funktionen**: GeoJSON, CSV, JSON-Statistiken
- **📍 LV95-Koordinaten**: Live-Anzeige beim Hover (Schweizer Landeskoordinaten)
- **📐 Messwerkzeuge**: Distanzen und Flächen messen
- **✨ Feature-Highlighting**: Gefundene Objekte werden auf Karte und Tabelle hervorgehoben
- **🗂️ Layer-Management**: Automatische Gruppierung nach Themen

## 📋 Anwendungsfälle

- **Qualitätskontrolle**: Schnelle Prüfung von Vermessungsdaten
- **Objekt-Suche**: Fixpunkte, Grenzpunkte, Gebäude schnell finden
- **Visualisierung**: Amtliche Vermessung interaktiv darstellen
- **Datenexport**: Gefilterte Daten für CAD/GIS exportieren
- **Präsentationen**: Geodaten anschaulich zeigen

## 🎯 Zielgruppe

- 📐 Vermessungsingenieure
- 🏗️ Bauingenieure
- 🗺️ GIS-Techniker
- 🏛️ Gemeinden & Kantone
- 👨‍💻 Geodaten-Entwickler

## 🚀 Quick Start

1. **Öffne** `index.html` im Browser
2. **Ziehe** deine GeoJSON-Datei auf das Upload-Feld
3. **Fertig!** Die Daten werden automatisch auf der Karte dargestellt

### Erwartetes GeoJSON-Format

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [2600000, 1200000]
    },
    "properties": {
      "table": "Lagefixpunkte2",
      "layer_name": "Lagefixpunkte 2. Ordnung",
      "layer_group": "Fixpunkte",
      "obj_id": "12345",
      "color": "#e74c3c",
      "symbol": "🎯"
    }
  }]
}
```

## 📖 Bedienung

### 🔍 Suche verwenden
1. Suchbegriff eingeben (z.B. Punkt-ID, Name)
2. **Enter** drücken oder **Suchen** klicken
3. Auf Ergebnis klicken → Zoom & Highlight

### 📊 Attribut-Tabelle
1. Button **📊 Tabelle** klicken
2. Auf Spalten-Header klicken zum Sortieren (▲▼)
3. Auf Zeile klicken → Zoom zum Feature
4. **CSV Export** für Excel/Calc

### 🎨 Layer stylen
1. **🎨** Symbol neben Layer klicken
2. Farbe, Grösse, Symbol, Deckkraft anpassen
3. **✅ Anwenden** klicken
4. Änderungen sind sofort sichtbar

### 💾 Daten exportieren
1. Button **💾 Export** klicken
2. Format wählen:
   - **GeoJSON** (alle Features)
   - **GeoJSON** (nur sichtbare Layer)
   - **CSV** (Attribut-Tabelle)
   - **JSON** (Statistiken)

## 🛠️ Technologie

- **Leaflet 1.9.4**: Interaktive Karten-Bibliothek
- **LV95 ↔ WGS84**: Automatische Koordinaten-Transformation
- **Client-Side**: Läuft komplett im Browser
- **Keine Installation**: Einfach HTML-Datei öffnen

## 📦 Installation

Keine Installation nötig! Einfach die `index.html` in einem modernen Browser öffnen.

### Für lokale Entwicklung (optional):
```bash
# Lokaler Server
python -m http.server 8000
# Öffne: http://localhost:8000
```

## 📄 Lizenz

MIT License - Frei verwendbar für kommerzielle und private Projekte.

---

*Optimiert für Schweizer Vermessungsdaten | LV95 | INTERLIS*
