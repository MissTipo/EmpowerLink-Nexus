import React from 'react';
import { useQuery } from '@apollo/client';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapChart.css';

// Direct import of the geojson file
import africaGeoJSON from '../../assets/africa_countries.json';
import { GET_RESOURCES_PER_CAPITA } from '../../graphql/queries';

const ResourceHeatMap = () => {
  const { data, loading, error } = useQuery(GET_RESOURCES_PER_CAPITA);

  if (loading) return <div>Loading heatmap...</div>;
  if (error) return <div>Error loading data 😢</div>;

  // Create a map of region names to the corresponding resources count
  const dataByRegion = {
    "Kenya": 8,
    "Uganda": 5,
    "Tanzania": 6,
    "South Africa": 7,
    "Nigeria": 9,
  };
  data.resourcesPerCapita.forEach((item) => {
    const regionName = item.regionName; // Assuming your API includes regionName field
    const totalServices = item.resourcesCount;
    dataByRegion[regionName] = totalServices;
  });

  const getColor = (value) => {
    return value > 8 ? '#084594' :
           value > 6 ? '#2171b5' :
           value > 4 ? '#4292c6' :
           value > 2 ? '#6baed6' :
                        '#c6dbef';
  };

  const style = (feature) => {
    const regionName = feature.properties.name;
    const value = dataByRegion[regionName] || 0;
    return {
      fillColor: getColor(value),
      weight: 1,
      opacity: 2,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.8,
    };
  };

  return (
    <div className="chart-card">
      <h3>Resources per 1,000 People by Region</h3>
      <MapContainer center={[0, 20]} zoom={3} style={{ height: '500px', width: '100%' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <GeoJSON data={africaGeoJSON} style={style} />
      </MapContainer>
    </div>
  );
};

export default ResourceHeatMap;

