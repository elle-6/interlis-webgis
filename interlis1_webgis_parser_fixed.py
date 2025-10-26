# interlis1_webgis_parser_fixed.py - KOMPLETT KORRIGIERT
"""
INTERLIS1 Parser für WebGIS mit verbesserter Polygon-Erkennung
"""

import json
import re
import os
from collections import defaultdict

def parse_for_webgis(filepath):
    """Parse INTERLIS1 für WebGIS mit verbesserter Geometrie-Erkennung"""
    
    print(f"📖 Lese INTERLIS1 Datei: {filepath}")
    
    with open(filepath, 'r', encoding='latin-1') as f:
        content = f.read()
    
    features = []
    table_info = defaultdict(lambda: {'count': 0, 'geometry_types': defaultdict(int), 'topics': set()})
    lines = content.split('\n')
    current_table = None
    current_topic = None
    current_geometry = []
    current_obj_id = None
    in_geometry = False
    geometry_type = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Topic-Start
        if line.startswith('TOPI '):
            current_topic = line.split()[1]
            continue
        
        # Tabellen-Start
        if line.startswith('TABL '):
            current_table = line.split()[1]
            continue
        
        # Tabellen-Ende
        if line == 'ETAB':
            current_table = None
            continue
        
        # Topic-Ende
        if line == 'ETOP':
            current_topic = None
            continue
        
        # OBJE Start - neues Objekt
        if line.startswith('OBJE '):
            # Vorherige Geometrie abschließen falls vorhanden
            if in_geometry and current_geometry and current_table:
                geometry_obj = create_geometry_object(current_geometry, geometry_type, current_table)
                if geometry_obj:
                    add_feature(features, table_info, current_table, current_topic, 
                               geometry_obj, current_geometry, current_obj_id)
            
            # Neues Objekt starten
            current_geometry = []
            in_geometry = False
            geometry_type = None
            current_obj_id = extract_obj_id(line)
            
            # Punkt-Geometrien direkt parsen
            point_features = parse_point_geometries_for_webgis(line, current_table, current_topic)
            for feature in point_features:
                table_info[current_table]['count'] += 1
                table_info[current_table]['geometry_types']['Point'] += 1
                if current_topic:
                    table_info[current_table]['topics'].add(current_topic)
                features.append(feature)
            continue
        
        # Geometrie-Start (STPT = Start Point)
        if line.startswith('STPT'):
            if not in_geometry:
                current_geometry = []
                in_geometry = True
                # Bestimme Geometrietyp basierend auf Tabellenname
                geometry_type = determine_geometry_type(current_table)
            
            coords = parse_coordinates_from_line(line)
            if coords:
                current_geometry.append(coords)
        
        # Linien-Punkte (LIPT = Line Point)
        elif line.startswith('LIPT') and in_geometry:
            coords = parse_coordinates_from_line(line)
            if coords:
                current_geometry.append(coords)
        
        # Geometrie-Ende (ELIN = End Line)
        elif line == 'ELIN' and in_geometry:
            if current_geometry and len(current_geometry) >= 2 and current_table:
                geometry_obj = create_geometry_object(current_geometry, geometry_type, current_table)
                if geometry_obj:
                    add_feature(features, table_info, current_table, current_topic, 
                               geometry_obj, current_geometry, current_obj_id)
            
            current_geometry = []
            in_geometry = False
            geometry_type = None
    
    print(f"✅ {len(features)} Features in {len(table_info)} Tabellen gefunden")
    return features, table_info

def determine_geometry_type(table_name):
    """Bestimme den Geometrietyp basierend auf Tabellenname"""
    if not table_name:
        return 'LineString'
    
    table_lower = table_name.lower()
    
    # Polygone für Flächen
    if any(keyword in table_lower for keyword in ['boflaeche', 'bodenbedeckung', 'flaeche', 'gebiet', 'perimeter']):
        return 'Polygon'
    # Linien für Grenzen und Kanten
    elif any(keyword in table_lower for keyword in ['grenze', 'kante', 'linie', 'strasse']):
        return 'LineString'
    else:
        return 'LineString'

def create_geometry_object(coordinates, geometry_type, table_name):
    """Erstelle korrektes GeoJSON Geometry-Objekt"""
    if not coordinates or len(coordinates) < 2:
        return None
    
    # Für Polygone: Stelle sicher, dass es geschlossen ist
    if geometry_type == 'Polygon':
        if len(coordinates) >= 3:
            # Schließe den Ring wenn nötig
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])
            
            # Validiere Polygon - mindestens 4 Punkte für geschlossenen Ring
            if len(coordinates) >= 4:
                return {
                    'type': 'Polygon',
                    'coordinates': [coordinates]
                }
        # Fallback zu LineString wenn Polygon nicht möglich
        return {
            'type': 'LineString',
            'coordinates': coordinates
        }
    
    # Für LineStrings
    elif geometry_type == 'LineString':
        return {
            'type': 'LineString',
            'coordinates': coordinates
        }
    
    return None

def add_feature(features, table_info, table, topic, geometry_obj, coordinates, obj_id=None):
    """Füge Feature zur Liste hinzu"""
    table_info[table]['count'] += 1
    table_info[table]['geometry_types'][geometry_obj['type']] += 1
    if topic:
        table_info[table]['topics'].add(topic)
    
    feature = {
        'type': 'Feature',
        'properties': {
            'table': table,
            'topic': topic or '',
            'geometry_type': geometry_obj['type'],
            'layer_name': get_layer_name(table),
            'layer_group': get_layer_group(table),
            'point_count': len(coordinates),
            'obj_id': obj_id or ''
        },
        'geometry': geometry_obj
    }
    features.append(feature)

def extract_obj_id(line):
    """Extrahiere Objekt-ID aus OBJE Zeile"""
    parts = line.split()
    return parts[1] if len(parts) > 1 else ''

def get_layer_name(table_name):
    """Erstelle lesbaren Layer-Namen aus Tabellenname"""
    # Entferne Nachführung etc.
    name = table_name.replace('Nachfuehrung', '').replace('_Perimeter', '')
    
    # Verbessere Lesbarkeit
    replacements = {
        'LFP': 'Lagefixpunkte',
        'HFP': 'Höhenfixpunkte', 
        'Gebaeude': 'Gebäude',
        'Grenzpunkt': 'Grenzpunkte',
        'Liegenschaft': 'Liegenschaften',
        'Strasse': 'Strassen',
        'Flurname': 'Flurnamen',
        'Ortsname': 'Ortsnamen',
        'BoFlaeche': 'Bodenbedeckung',
        'Hoehenpunkt': 'Höhenpunkte',
        'Einzelpunkt': 'Einzelpunkte'
    }
    
    for key, value in replacements.items():
        if key in name:
            name = name.replace(key, value)
    
    return name.strip('_')

def get_layer_group(table_name):
    """Gruppiere Tabellen in Kategorien"""
    if any(keyword in table_name for keyword in ['LFP', 'HFP', 'Fixpunkt']):
        return 'Vermessung'
    elif any(keyword in table_name for keyword in ['Gebaeude', 'Hausnummer', 'Strasse']):
        return 'Gebäude & Adressen'
    elif any(keyword in table_name for keyword in ['Grenz', 'Liegenschaft', 'Grundstueck']):
        return 'Liegenschaften'
    elif any(keyword in table_name for keyword in ['BoFlaeche', 'Flaeche']):
        return 'Bodenbedeckung'
    elif any(keyword in table_name for keyword in ['Flurname', 'Ortsname', 'Gelaendename']):
        return 'Namen'
    elif any(keyword in table_name for keyword in ['Hoehen', 'Gelaendekante']):
        return 'Höhen'
    elif any(keyword in table_name for keyword in ['Einzelobjekt', 'Punktelement']):
        return 'Einzelobjekte'
    else:
        return 'Sonstige'

def parse_coordinates_from_line(line):
    """Parse Koordinaten aus Geometrie-Zeilen"""
    parts = line.split()
    if len(parts) >= 3:
        try:
            e = float(parts[1])
            n = float(parts[2])
            if 2000000 < e < 3000000 and 1000000 < n < 1300000:
                return [e, n]
        except (ValueError, IndexError):
            pass
    return None

def parse_point_geometries_for_webgis(line, table, topic):
    """Parse Punkt-Geometrien für WebGIS"""
    features = []
    
    line_clean = re.sub(r'\\\s*\n\s*CONT', ' ', line)
    line_clean = line_clean.replace('OBJE ', '')
    
    parts = re.split(r'\s+', line_clean)
    parts = [p for p in parts if p and p != '@']
    
    if len(parts) < 5:
        return features
    
    # Suche nach Koordinaten
    for i in range(len(parts) - 1):
        try:
            e = float(parts[i])
            n = float(parts[i+1])
            
            if 2000000 < e < 3000000 and 1000000 < n < 1300000:
                # Höhe
                h = None
                if i+2 < len(parts):
                    try:
                        h_candidate = float(parts[i+2])
                        if 0 < h_candidate < 5000:
                            h = h_candidate
                    except ValueError:
                        pass
                
                # Bestimme Symbol und Farbe
                symbol, color = get_point_style(table)
                
                properties = {
                    'table': table,
                    'topic': topic or '',
                    'geometry_type': 'Point',
                    'layer_name': get_layer_name(table),
                    'layer_group': get_layer_group(table),
                    'obj_id': parts[0],
                    'ident': parts[1] if len(parts) > 1 and parts[1] != '@' else '',
                    'nummer': parts[2] if len(parts) > 2 and parts[2] != '@' else '',
                    'hoehe': h,
                    'symbol': symbol,
                    'color': color
                }
                
                feature = {
                    'type': 'Feature',
                    'properties': properties,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [e, n]
                    }
                }
                features.append(feature)
                break
                
        except (ValueError, IndexError):
            continue
    
    return features

def get_point_style(table_name):
    """Bestimme Symbol und Farbe basierend auf Tabelle"""
    if 'LFP' in table_name:
        return '📐', '#e74c3c'  # Rot für Fixpunkte
    elif 'HFP' in table_name:
        return '⛰️', '#3498db'  # Blau für Höhenpunkte
    elif 'Gebaeude' in table_name:
        return '🏠', '#9b59b6'  # Lila für Gebäude
    elif 'Grenz' in table_name:
        return '📍', '#f39c12'  # Orange für Grenzpunkte
    elif 'Hausnummer' in table_name:
        return '🏘️', '#e67e22'  # Braun für Hausnummern
    elif 'Strasse' in table_name:
        return '🛣️', '#34495e'  # Dunkelgrau für Strassen
    else:
        return '📌', '#95a5a6'  # Grau für andere

def convert_sets_to_lists(obj):
    """Konvertiere sets zu lists für JSON Serialisierung"""
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    else:
        return obj

def create_webgis_output(features, table_info):
    """Erstelle WebGIS-kompatibles Output"""
    
    print("\n🗺️  Erstelle WebGIS Output...")
    
    # Statistik
    total_features = len(features)
    geometry_stats = defaultdict(int)
    group_stats = defaultdict(int)
    
    for feature in features:
        geometry_stats[feature['geometry']['type']] += 1
        group_stats[feature['properties']['layer_group']] += 1
    
    print(f"📊 WebGIS Statistik:")
    print(f"   • Gesamt Features: {total_features}")
    print(f"   • Geometrietypen:")
    for geom_type, count in geometry_stats.items():
        print(f"     - {geom_type}: {count}")
    print(f"   • Layergruppen:")
    for group, count in group_stats.items():
        print(f"     - {group}: {count}")
    
    print(f"\n📋 Tabellen-Übersicht:")
    for table, info in sorted(table_info.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
        geom_types = ', '.join([f"{k}:{v}" for k, v in info['geometry_types'].items()])
        print(f"   • {table}: {info['count']} Features ({geom_types})")
    
    # Konvertiere sets zu lists für JSON
    table_info_serializable = convert_sets_to_lists(table_info)
    
    # GeoJSON erstellen
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:2056"
            }
        },
        "metadata": {
            "total_features": total_features,
            "tables": table_info_serializable,
            "geometry_stats": dict(geometry_stats),
            "group_stats": dict(group_stats),
            "layer_groups": list(group_stats.keys())
        },
        "features": features
    }
    
    return geojson

def main():
    """Hauptfunktion"""
    
    print("=" * 60)
    print("🗺️  INTERLIS1 WebGIS Parser - FIXED")
    print("=" * 60)
    
    input_file = '7-knonau-gds.itf'
    output_file = 'webgis_data.geojson'
    
    try:
        # Parse für WebGIS
        features, table_info = parse_for_webgis(input_file)
        
        if not features:
            print("\n⚠️  Keine Features gefunden!")
            return
        
        # WebGIS Output erstellen
        geojson = create_webgis_output(features, table_info)
        
        # Speichern
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ WebGIS Data gespeichert: {output_file}")
        print(f"   → {len(features)} Features")
        print(f"   → {len(table_info)} Tabellen")
        print(f"   → Layergruppen: {len(geojson['metadata']['group_stats'])}")
        
        print("\n" + "=" * 60)
        print("✅ FERTIG! WebGIS Data generiert.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()