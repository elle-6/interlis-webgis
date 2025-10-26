# 🗺️ INTERLIS1 WebGIS

Ein komplettes Tool-Set zur Verarbeitung und Visualisierung von Schweizer Vermessungsdaten: Python-Parser für INTERLIS1-Dateien (.itf) + interaktives WebGIS im Browser.

## 📦 Komponenten

### 1. 🐍 Python Parser (`interlis1_webgis_parser_fixed.py`)
Konvertiert INTERLIS1-Dateien zu WebGIS-kompatiblem GeoJSON.

### 2. 🌐 WebGIS (`index.html`)
Interaktive Karten-Anwendung zur Visualisierung und Analyse.

---

## 🔄 Workflow

```
.itf Datei (INTERLIS1)
        ↓
   interlis1_webgis_parser_fixed.py
        ↓
webgis_data.geojson
        ↓
   index.html (Browser)
        ↓
   Interaktive Karte
```

---

## 🐍 Python Parser

### Features
- **INTERLIS1 Parsing**: Verarbeitet .itf-Dateien mit LV95-Koordinaten (EPSG:2056)
- **Geometrie-Typen**: Punkte, Linien und korrekt geschlossene Polygone
- **GeoJSON Export**: WebGIS-kompatible Ausgabe
- **Layer-Management**: Automatische Gruppierung nach Themen
- **Styling**: Automatische Farben & Symbole-Zuweisung
- **Tabellen-Übersicht**: Metadaten zu allen INTERLIS-Tabellen

### Installation

```bash
# Repository klonen
git clone https://github.com/DEIN-USERNAME/interlis-webgis.git
cd interlis-webgis

# Abhängigkeiten installieren (falls nötig)
pip install -r requirements.txt
```

### Verwendung

```bash
# INTERLIS1 zu GeoJSON konvertieren
python interlis1_webgis_parser_fixed.py input.itf

# Output: webgis_data.geojson
```

### Input-Format (.itf)
```
INTERLIS 1.0
MODL DM01AVCH24D
TOPI Bodenbedeckung
TABL BoFlaeche
OBJE 1234
GEOS 2600000.000 1200000.000
...
```

### Output-Format (GeoJSON)
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
      "layer_name": "Lagefixpunkte",
      "layer_group": "Fixpunkte",
      "color": "#e74c3c",
      "symbol": "🎯"
    }
  }]
}
```

---

## 🌐 WebGIS

### Features

- **📁 Drag & Drop**: GeoJSON-Dateien einfach laden
- **🔍 Intelligente Suche**: Durchsucht alle Feature-Attribute
- **📊 Attribut-Tabelle**: Sortierbar mit CSV-Export
- **🎨 Style-Editor**: Individuelle Farben, Größen & Symbole pro Layer
- **💾 Export-Funktionen**: GeoJSON, CSV, JSON-Statistiken
- **📍 LV95-Koordinaten**: Live-Anzeige beim Hover
- **📐 Messwerkzeuge**: Distanzen und Flächen messen
- **✨ Feature-Highlighting**: Objekte auf Karte und Tabelle hervorheben
- **🗂️ Layer-Management**: Automatische Gruppierung

### Verwendung

```bash
# 1. GeoJSON mit Parser erstellen
python interlis1_webgis_parser_fixed.py meine_daten.itf

# 2. WebGIS öffnen
# Öffne index.html im Browser

# 3. webgis_data.geojson auf Upload-Feld ziehen

# 4. Fertig!
```

### Bedienung

**🔍 Suche:**
- Suchbegriff eingeben → Enter → Ergebnis anklicken

**📊 Tabelle:**
- Button "📊 Tabelle" → Spalten sortieren → Zeile anklicken

**🎨 Styling:**
- 🎨 neben Layer klicken → Anpassen → ✅ Anwenden

**💾 Export:**
- Button "💾 Export" → Format wählen

---

## 📁 Projektstruktur

```
interlis-webgis/
├── interlis1_webgis_parser_fixed.py   # INTERLIS1 → GeoJSON Konverter
├── index.html                         # WebGIS-Anwendung
├── README.md                          # Diese Dokumentation
├── 7-knonau-gds.itf                   # Beispiel-Dateien
└── webgis_data.geojson                # Beispiel-Dateien

```

---

## 🎯 Anwendungsfälle

- **Qualitätskontrolle**: Vermessungsdaten schnell prüfen
- **Objekt-Suche**: Fixpunkte, Grenzpunkte finden
- **Visualisierung**: Amtliche Vermessung darstellen
- **Datenexport**: Gefilterte Daten für CAD/GIS
- **Präsentationen**: Geodaten anschaulich zeigen

## 👥 Zielgruppe

- 📐 Vermessungsingenieure
- 🏗️ Bauingenieure
- 🗺️ GIS-Techniker
- 🏛️ Gemeinden & Kantone
- 👨‍💻 Geodaten-Entwickler

---

## 🛠️ Technologie

### Python Parser
- Python 3.8+
- LV95-Koordinaten (EPSG:2056)
- GeoJSON-Standard

### WebGIS
- Leaflet 1.9.4
- LV95 ↔ WGS84 Transformation
- Client-Side (keine Server nötig)

---

## 🚀 Quick Start (Kompletter Workflow)

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/interlis-webgis.git
cd interlis-webgis

# 2. INTERLIS-Datei konvertieren
python parser.py deine_daten.itf

# 3. WebGIS starten
python -m http.server 8000

# 4. Browser öffnen
# http://localhost:8000

# 5. webgis_data.geojson auf die Seite ziehen

# Fertig! 🎉
```

---

## 📄 Lizenz

MIT License - Frei verwendbar für kommerzielle und private Projekte.

---

**Made with ❤️ for Swiss Geodata** 🇨🇭

*INTERLIS1 | LV95 | Amtliche Vermessung*
