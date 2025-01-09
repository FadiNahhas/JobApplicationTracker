from PyQt6.QtWidgets import QDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from UI.map_dialog import Ui_mapDialog
import json
from constants import STATUS_PENDING, STATUS_ACTIVE, STATUS_CLOSED
from config import GOOGLE_MAPS_API_KEY
import math

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
        """
        Create the HTML content for the map display.
        
        Args:
            applications: List of Application objects to display on map
        """
        # Create markers data
        markers = []
        bounds: dict[str, float] = {
            'north': -90.0,
            'south': 90.0,
            'east': -180.0,
            'west': 180.0
        }
        
        # Filter out closed applications and collect markers
        active_applications = [app for app in applications if app.status != STATUS_CLOSED]
        
        # Group applications by location to handle overlapping
        location_groups = {}
        for app in active_applications:
            if app.location and app.latitude and app.longitude:
                key = f"{app.latitude},{app.longitude}"
                if key not in location_groups:
                    location_groups[key] = []
                location_groups[key].append(app)
        
        # Create markers with offsets for overlapping locations
        for key, apps in location_groups.items():
            base_lat, base_lng = map(float, key.split(','))
            
            for i, app in enumerate(apps):
                # Create spiral pattern for multiple markers at same location
                angle = i * (2 * math.pi / 8)  # 8 positions around the point
                radius = 0.005 * (1 + (i // 8))  # Increased radius for more visible spread
                
                marker_lat = base_lat + (radius * math.cos(angle))
                marker_lng = base_lng + (radius * math.sin(angle))
                
                color = {
                    STATUS_PENDING: '#FFD700',  # Yellow
                    STATUS_ACTIVE: '#00FF00',   # Green
                    STATUS_CLOSED: '#FF0000'    # Red
                }.get(app.status, '#FF0000')
                
                markers.append({
                    'lat': marker_lat,
                    'lng': marker_lng,
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
                
                # Update bounds
                bounds['north'] = max(bounds['north'], marker_lat)
                bounds['south'] = min(bounds['south'], marker_lat)
                bounds['east'] = max(bounds['east'], marker_lng)
                bounds['west'] = min(bounds['west'], marker_lng)
        
        # Create the HTML template with the markers and bounds
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Job Applications Map</title>
                <script>
                    const markers = {json.dumps(markers)};
                    const mapBounds = {json.dumps(bounds)};
                    let activeMarkers = [];
                    let map;
                    
                    function updateMarkerPositions() {{
                        const zoom = map.getZoom();
                        const spreadFactor = Math.max(0.5 / Math.pow(1.5, zoom - 2), 0.001);
                        
                        markers.forEach((marker, i) => {{
                            const basePos = new google.maps.LatLng(marker.lat, marker.lng);
                            const angle = i * (2 * Math.PI / 8);
                            const ring = Math.floor(i / 8);
                            const radius = spreadFactor * (1 + ring);
                            
                            const newLat = marker.lat + (radius * Math.cos(angle));
                            const newLng = marker.lng + (radius * Math.sin(angle));
                            
                            if (activeMarkers[i]) {{
                                activeMarkers[i].setPosition(new google.maps.LatLng(newLat, newLng));
                            }}
                        }});
                    }}
                    
                    function initMap() {{
                        map = new google.maps.Map(document.getElementById('map'));
                        const bounds = new google.maps.LatLngBounds(
                            new google.maps.LatLng(mapBounds.south, mapBounds.west),
                            new google.maps.LatLng(mapBounds.north, mapBounds.east)
                        );
                        
                        markers.forEach((marker, i) => {{
                            const mapMarker = new google.maps.Marker({{
                                position: new google.maps.LatLng(marker.lat, marker.lng),
                                map: map,
                                title: marker.title,
                                icon: {{
                                    path: google.maps.SymbolPath.CIRCLE,
                                    scale: 8,
                                    fillColor: marker.color,
                                    fillOpacity: 0.8,
                                    strokeWeight: 1
                                }}
                            }});
                            
                            activeMarkers.push(mapMarker);
                            
                            const infoWindow = new google.maps.InfoWindow({{
                                content: marker.info
                            }});
                            
                            mapMarker.addListener('click', () => {{
                                infoWindow.open(map, mapMarker);
                            }});
                        }});
                        
                        map.fitBounds(bounds);
                        
                        // Update markers when zoom changes
                        map.addListener('zoom_changed', updateMarkerPositions);
                        // Initial position update
                        google.maps.event.addListenerOnce(map, 'idle', updateMarkerPositions);
                    }}
                </script>
                <script async defer
                    src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap">
                </script>
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
                </style>
            </head>
            <body>
                <div id="map"></div>
            </body>
            </html>
        """

    def get_status_color(self, status):
        return {
            STATUS_PENDING: '#FFD700',  # Yellow
            STATUS_ACTIVE: '#00FF00',   # Green
            STATUS_CLOSED: '#FF0000'    # Red
        }.get(status, '#FF0000')    # Default to red if status unknown

    def create_info_window_content(self, app):
        return f"""
            <div style='padding: 8px; max-width: 200px'>
                <h3 style='margin: 0 0 8px 0'>{app.company}</h3>
                <p style='margin: 4px 0'><b>Job:</b> {app.job_title}</p>
                <p style='margin: 4px 0'><b>Location:</b> {app.location}</p>
                <p style='margin: 4px 0'><b>Status:</b> {app.status}</p>
                <p style='margin: 4px 0'><b>Applied:</b> {app.application_date}</p>
            </div>
        """
