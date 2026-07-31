import React from 'react';
import LiveMap from './components/LiveMap';
import ReviewQueue from './components/ReviewQueue';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col font-sans">
      <header className="bg-gray-900 border-b border-gray-800 p-4 shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400">
              Disaster Resource Coordinator
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-gray-400 bg-gray-800 px-3 py-1.5 rounded-full border border-gray-700">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span>Backend Connected</span>
            </div>
            <button className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium border border-gray-700 transition-colors">
              Admin Dashboard
            </button>
          </div>
        </div>
      </header>
      
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Live Map (Takes 2/3 space on large screens) */}
        <div className="lg:col-span-2 flex flex-col min-h-[500px]">
          <LiveMap />
        </div>
        
        {/* Right Column - Review Queue (Takes 1/3 space on large screens) */}
        <div className="flex flex-col">
          <ReviewQueue />
        </div>
      </main>
    </div>
  );
}

export default App;
