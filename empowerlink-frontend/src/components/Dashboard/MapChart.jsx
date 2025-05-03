import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapChart.css';
import L from 'leaflet';
import markerIcon from '../../assets/logo.png';

// Fix Leaflet default icon issue with Webpack
const customIcon = new L.Icon({
  iconUrl: markerIcon,
  iconSize: [35, 35],
  iconAnchor: [17, 34],
  popupAnchor: [0, -30],
});

export default function MapChart() {
  const positions = [
    { lat: -1.286389, lng: 36.817223, label: 'Nairobi HQ' },
    { lat: 0.347596, lng: 32.582520, label: 'Kampala' },
    { lat: -6.792354, lng: 39.208328, label: 'Dar es Salaam' },
  ];

  return (
    <div className="map-chart">
      <h3 className="map-title">Inclusivity Map</h3>
      <MapContainer center={[-1.286389, 36.817223]} zoom={5} scrollWheelZoom={false} className="map-container">
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {positions.map((pos, index) => (
          <Marker key={index} position={[pos.lat, pos.lng]} icon={customIcon}>
            <Popup>{pos.label}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

