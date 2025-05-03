// src/components/Dashboard/MapChart.jsx
import React from 'react'
import './MapChartNew.css';
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker
} from "react-simple-maps";

// a small GeoJSON of the world (you can host your own or use the CDN)
const GEO_URL =
  "https://unpkg.com/world-atlas@2.0.2/countries-50m.json";

const points = [
  { name: "Nairobi HQ", coordinates: [36.817223, -1.286389] },
  { name: "Kampala", coordinates: [32.58252, 0.347596] },
  { name: "Dar es Salaam", coordinates: [39.208328, -6.792354] },
];

export default function MapChart() {
  return (
    <div className="map-chart">
      <ComposableMap
        projectionConfig={{ scale: 130 }}
        style={{ width: "100%", height: "auto" }}
      >
        <Geographies geography={GEO_URL}>
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#EAEAEC"
                stroke="#D6D6DA"
              />
            ))
          }
        </Geographies>

        {points.map(({ name, coordinates }, idx) => (
          <Marker key={idx} coordinates={coordinates}>
            <circle r={5} fill="#017C8C" stroke="#fff" strokeWidth={1} />
            <text
              textAnchor="middle"
              y={-10}
              style={{
                fontFamily: "var(--font-family-base)",
                fill: "var(--color-on-surface)",
                fontSize: "0.75rem"
              }}
            >
              {name}
            </text>
          </Marker>
        ))}
      </ComposableMap>
    </div>
  );
}

