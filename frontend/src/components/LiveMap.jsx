import React from 'react';

// Using a placeholder map since leaflet isn't installed yet. 
// A production version would use react-leaflet.
const LiveMap = () => {
  return (
    <div className="bg-gray-900 rounded-xl shadow-2xl overflow-hidden border border-gray-800 h-full flex flex-col">
      <div className="p-4 bg-gray-800/80 border-b border-gray-700 flex justify-between items-center backdrop-blur-md">
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
      
      <div className="flex-1 relative bg-gray-950 flex items-center justify-center p-8">
        {/* Abstract Map Visualization */}
        <div className="absolute inset-0 opacity-20" style={{
          backgroundImage: 'radial-gradient(circle at center, #3b82f6 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }}></div>
        
        <div className="relative z-10 w-full max-w-lg">
          <div className="aspect-[4/3] bg-gray-800/50 rounded-2xl border border-gray-700 p-4 backdrop-blur flex flex-col items-center justify-center relative overflow-hidden">
            
            {/* Animated pings */}
            <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-red-500 rounded-full shadow-[0_0_15px_rgba(239,68,68,0.8)]">
              <div className="absolute inset-0 bg-red-500 rounded-full animate-ping opacity-75"></div>
            </div>
            
            <div className="absolute top-1/2 right-1/3 w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.8)]">
              <div className="absolute inset-0 bg-blue-500 rounded-full animate-ping opacity-75" style={{ animationDelay: '1s' }}></div>
            </div>
            
            <div className="absolute bottom-1/4 right-1/4 w-3 h-3 bg-green-500 rounded-full shadow-[0_0_15px_rgba(34,197,94,0.8)]">
              <div className="absolute inset-0 bg-green-500 rounded-full animate-ping opacity-75" style={{ animationDelay: '0.5s' }}></div>
            </div>

            {/* Connection lines */}
            <svg className="absolute inset-0 w-full h-full opacity-30 pointer-events-none">
              <path d="M 25% 25% L 66% 50%" stroke="#3b82f6" strokeWidth="2" strokeDasharray="5,5" fill="none" className="animate-[dash_2s_linear_infinite]" />
              <path d="M 66% 50% L 75% 75%" stroke="#22c55e" strokeWidth="2" strokeDasharray="5,5" fill="none" className="animate-[dash_2s_linear_infinite]" />
            </svg>
            
            <div className="text-center mt-auto mb-auto bg-gray-900/80 p-4 rounded-xl border border-gray-700">
              <h3 className="text-white font-medium mb-1">Simulated Area</h3>
              <p className="text-gray-400 text-sm">Waiting for actual coordinates from backend...</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-900 border-t border-gray-800 p-4">
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
