from PyQt6.QtWidgets import QDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from UI.map_dialog import Ui_mapDialog
import json
from constants import STATUS_PENDING, STATUS_CLOSED, STATUS_ACTIVE
from config import GOOGLE_MAPS_API_KEY

class MapDialog(QDialog, Ui_mapDialog):
    def __init__(self, applications):
        super().__init__()
        self.setupUi(self)
        
        # Create web view and set size before loading content
        self.web_view = QWebEngineView()
        self.mapLayout.addWidget(self.web_view)
        self.resize(800, 600)
        
        # Generate and load the map
        html = self.create_map_html(applications)
        self.web_view.setHtml(html)

    def create_map_html(self, applications):
        # Create markers data
        markers = []
        bounds = {
            'north': -90,
            'south': 90,
            'east': -180,
            'west': 180
        }
        
        for app in applications:
            if app.location and app.latitude and app.longitude:
                # Set marker color based on status
                color = {
                    STATUS_PENDING: '#FFD700',  # Yellow
                    STATUS_ACTIVE: '#00FF00',   # Green
                    STATUS_CLOSED: '#FF0000'    # Red
                }.get(app.status, '#FF0000')    # Default to red if status unknown
                
                markers.append({
                    'lat': app.latitude,
                    'lng': app.longitude,
                    'title': app.company,
                    'color': color,
                    'info': f"""
                        <div style='padding: 8px; max-width: 200px'>
                            <h3 style='margin: 0 0 8px 0'>{app.company}</h3>
                            <p style='margin: 4px 0'><b>Job:</b> {app.job_title}</p>
                            <p style='margin: 4px 0'><b>Location:</b> {app.location}</p>
                            <p style='margin: 4px 0'><b>Status:</b> {app.status}</p>
                            <p style='margin: 4px 0'><b>Applied:</b> {app.application_date}</p>
                        </div>
                    """
                })
                bounds['north'] = max(bounds['north'], app.latitude)
                bounds['south'] = min(bounds['south'], app.latitude)
                bounds['east'] = max(bounds['east'], app.longitude)
                bounds['west'] = min(bounds['west'], app.longitude)

        if not markers:
            bounds = {
                'north': 75,
                'south': -60,
                'east': 180,
                'west': -180
            }

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Applications Map</title>
            <style>
                html, body {{
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
                #map {{
                    height: 100%;
                    width: 100%;
                }}
                .gm-style-iw button {{
                    display: none !important;
                }}
                .gm-style-iw-d {{
                    overflow: hidden !important;
                }}
                .gm-style-iw {{
                    padding: 0 !important;
                }}
            </style>
            <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}"></script>
            <script>
                function initMap() {{
                    const bounds = {json.dumps(bounds)};
                    
                    const map = new google.maps.Map(document.getElementById('map'), {{
                        mapTypeId: google.maps.MapTypeId.ROADMAP,
                        restriction: {{
                            latLngBounds: {{
                                north: 85,
                                south: -85,
                                west: -180,
                                east: 180
                            }},
                            strictBounds: true
                        }},
                        minZoom: 2,
                        streetView: null,
                        streetViewControl: false,
                        mapTypeControl: false,
                        fullscreenControl: false,
                        zoomControl: true,
                        zoomControlOptions: {{
                            position: google.maps.ControlPosition.RIGHT_CENTER
                        }}
                    }});

                    const mapBounds = new google.maps.LatLngBounds(
                        new google.maps.LatLng(bounds.south, bounds.west),
                        new google.maps.LatLng(bounds.north, bounds.east)
                    );
                    map.fitBounds(mapBounds, 50);

                    const markers = {json.dumps(markers)};
                    
                    markers.forEach(marker => {{
                        const infowindow = new google.maps.InfoWindow({{
                            content: marker.info,
                            disableAutoPan: true
                        }});

                        const mapMarker = new google.maps.Marker({{
                            position: {{lat: marker.lat, lng: marker.lng}},
                            map: map,
                            title: marker.title,
                            icon: {{
                                path: google.maps.SymbolPath.CIRCLE,
                                fillColor: marker.color,
                                fillOpacity: 1,
                                strokeWeight: 1,
                                strokeColor: '#000000',
                                scale: 10
                            }}
                        }});

                        mapMarker.addListener('mouseover', () => {{
                            infowindow.open({{
                                map,
                                anchor: mapMarker,
                                shouldFocus: false
                            }});
                        }});

                        mapMarker.addListener('mouseout', () => {{
                            infowindow.close();
                        }});
                    }});
                }}

                window.onload = initMap;
            </script>
        </head>
        <body>
            <div id="map"></div>
        </body>
        </html>
        """
