'use client';

import React, { useEffect, useState } from 'react';
import { MapPin, Layers, RefreshCw } from 'lucide-react';

interface WeatherMapProps {
  location: { name: string; lat: number; lon: number };
  onMapClick: (lat: number, lon: number) => void;
}

export const WeatherMap: React.FC<WeatherMapProps> = ({ location, onMapClick }) => {
  const [activeLayer, setActiveLayer] = useState<'temp' | 'rain' | 'wind'>('temp');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return (
      <div className="h-64 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-center text-xs text-slate-500">
        Loading Interactive GIS Map...
      </div>
    );
  }

  // Dynamic Leaflet import to prevent SSR issues
  const { MapContainer, TileLayer, Marker, Popup, useMapEvents } = require('react-leaflet');
  const L = require('leaflet');

  // Custom marker icon
  const customIcon = L.divIcon({
    className: 'custom-map-pin',
    html: `<div style="background-color: #0284c7; width: 18px; height: 18px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(2, 132, 199, 0.8);"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9]
  });

  const MapClickHandler = () => {
    useMapEvents({
      click(e: any) {
        onMapClick(e.latlng.lat, e.latlng.lng);
      },
    });
    return null;
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3 shadow-lg relative overflow-hidden">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-1.5 text-xs text-white font-medium">
          <MapPin className="w-4 h-4 text-sky-400" />
          <span>Interactive GIS Weather Canvas</span>
        </div>

        {/* Layer Controls */}
        <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-lg text-[10px]">
          <button
            onClick={() => setActiveLayer('temp')}
            className={`px-2 py-0.5 rounded ${activeLayer === 'temp' ? 'bg-sky-500 text-white font-semibold' : 'text-slate-400 hover:text-white'}`}
          >
            🌡️ Temp
          </button>
          <button
            onClick={() => setActiveLayer('rain')}
            className={`px-2 py-0.5 rounded ${activeLayer === 'rain' ? 'bg-sky-500 text-white font-semibold' : 'text-slate-400 hover:text-white'}`}
          >
            🌧️ Rain
          </button>
          <button
            onClick={() => setActiveLayer('wind')}
            className={`px-2 py-0.5 rounded ${activeLayer === 'wind' ? 'bg-sky-500 text-white font-semibold' : 'text-slate-400 hover:text-white'}`}
          >
            💨 Wind
          </button>
        </div>
      </div>

      <div className="h-64 w-full rounded-lg overflow-hidden border border-slate-700/60 relative">
        <MapContainer
          center={[location.lat, location.lon]}
          zoom={8}
          scrollWheelZoom={false}
          style={{ height: '100%', width: '100%' }}
        >
          {/* Base Tiles (CartoDB Dark Matter) */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />

          <MapClickHandler />

          <Marker position={[location.lat, location.lon]} icon={customIcon}>
            <Popup className="text-xs font-semibold">
              {location.name} ({location.lat.toFixed(2)}, {location.lon.toFixed(2)})
            </Popup>
          </Marker>
        </MapContainer>

        <div className="absolute bottom-2 left-2 bg-slate-900/90 border border-slate-700 px-2 py-1 rounded text-[10px] text-slate-300 backdrop-blur-md z-[1000]">
          💡 Click anywhere on map to query WeatherGPT for coordinates
        </div>
      </div>
    </div>
  );
};
