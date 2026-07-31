import React, { useState, useEffect } from 'react';

const ReviewQueue = () => {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock fetching queue for now
  useEffect(() => {
    setTimeout(() => {
      setQueue([
        {
          need_id: 'need-123',
          raw_text: 'Send 50 blankets to the main shelter on 5th st',
          urgency: 'HIGH',
          confidence: 0.3, // low confidence triggered review
          extracted_type: 'SHELTER_SUPPLIES',
        },
        {
          need_id: 'need-456',
          raw_text: 'I think we need medical kits here but not sure',
          urgency: 'MEDIUM',
          confidence: 0.1,
          extracted_type: 'MEDICAL',
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleAction = (id, action) => {
    // Optimistic update
    setQueue(prev => prev.filter(item => item.need_id !== id));
    // In real app, call API POST /review/{id}
    console.log(`Action ${action} for need ${id}`);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900 rounded-xl shadow-2xl p-6 border border-gray-800">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <span className="bg-orange-500/20 text-orange-400 p-2 rounded-lg mr-3">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        </span>
        Human Review Queue
      </h2>
      
      {queue.length === 0 ? (
        <div className="text-center text-gray-500 py-10">
          No items pending review.
        </div>
      ) : (
        <div className="space-y-4">
          {queue.map(item => (
            <div key={item.need_id} className="bg-gray-800 rounded-lg p-5 border border-gray-700 hover:border-gray-600 transition-colors">
              <div className="flex justify-between items-start mb-3">
                <span className="text-xs font-mono text-gray-400">{item.need_id}</span>
                <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                  item.urgency === 'CRITICAL' ? 'bg-red-500/20 text-red-400' : 
                  item.urgency === 'HIGH' ? 'bg-orange-500/20 text-orange-400' : 'bg-yellow-500/20 text-yellow-400'
                }`}>
                  {item.urgency}
                </span>
              </div>
              
              <div className="mb-4">
                <p className="text-gray-200 font-medium italic border-l-4 border-gray-600 pl-3 py-1">
                  "{item.raw_text}"
                </p>
              </div>
              
              <div className="flex items-center gap-4 text-sm text-gray-400 mb-5">
                <div className="flex items-center gap-1">
                  <span className="font-semibold text-gray-300">Extracted:</span> {item.extracted_type}
                </div>
                <div className="flex items-center gap-1">
                  <span className="font-semibold text-gray-300">Confidence:</span> 
                  <span className="text-red-400">{(item.confidence * 100).toFixed(0)}%</span>
                </div>
              </div>
              
              <div className="flex gap-3">
                <button 
                  onClick={() => handleAction(item.need_id, 'approve')}
                  className="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                  Approve
                </button>
                <button 
                  onClick={() => handleAction(item.need_id, 'reject')}
                  className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                  Reject & Edit
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReviewQueue;
