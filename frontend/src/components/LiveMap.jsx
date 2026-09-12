import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import client from '../api/client';
import L from 'leaflet';

// Fix for default marker icon in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const blueIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const LiveMap = () => {
  const [resources, setResources] = useState([]);
  const [queue, setQueue] = useState([]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [resReq, queueReq] = await Promise.all([
        client.get('/resources'),
        client.get('/needs/pending-review')
      ]);
      setResources(resReq.data.resources || []);
      setQueue(queueReq.data.queue || []);
    } catch (err) {
      console.error('Error fetching map data', err);
    }
  };

  // Default to a central location if no data
  const center = [40.7128, -74.0060]; // NYC

  return (
    <div className="bg-gray-900 rounded-xl shadow-2xl overflow-hidden border border-gray-800 h-full flex flex-col relative z-0">
      <div className="p-4 bg-gray-800/80 border-b border-gray-700 flex justify-between items-center backdrop-blur-md relative z-10">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Live Dispatch Map
        </h2>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-green-500/20 text-green-400 text-xs font-bold rounded-full flex items-center gap-1">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            System Active
          </span>
        </div>
      </div>
      
      <div className="flex-1 relative z-0">
        <MapContainer 
          center={center} 
          zoom={12} 
          style={{ height: '100%', width: '100%' }}
          zoomControl={false}
          className="z-0"
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          />
          
          {resources.map(res => {
            if (!res.lat || !res.lon) return null;
            return (
              <Marker key={res.resource_id} position={[res.lat, res.lon]} icon={blueIcon}>
                <Popup className="text-gray-900">
                  <div className="font-bold">{res.resource_type}</div>
                  <div>Qty: {res.quantity_available}</div>
                  <div className="text-xs text-gray-500">{res.resource_id}</div>
                </Popup>
              </Marker>
            );
          })}

          {queue.map(need => {
            if (!need.lat || !need.lon) return null;
            return (
              <Marker key={need.need_id} position={[need.lat, need.lon]} icon={redIcon}>
                <Popup className="text-gray-900">
                  <div className="font-bold text-red-600">Pending Need: {need.need_type}</div>
                  <div>Qty: {need.quantity_estimate}</div>
                  <div className="text-xs text-gray-500">{need.urgency}</div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>
      
      <div className="bg-gray-900 border-t border-gray-800 p-4 relative z-10">
        <div className="flex justify-around text-xs text-gray-400">
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-red-500"></span> Unmet Needs</div>
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-blue-500"></span> Resources</div>
          <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-green-500"></span> En Route</div>
        </div>
      </div>
    </div>
  );
};

export default LiveMap;