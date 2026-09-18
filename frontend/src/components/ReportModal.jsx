import React, { useState } from 'react';
import client from '../api/client';

const ReportModal = ({ onClose }) => {
  const [text, setText] = useState('');
  const [channel, setChannel] = useState('sms');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await client.post('/reports', {
        source_channel: channel,
        raw_text: text,
      });
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit report');
      setLoading(false);
    }
  };

  const loadPreset = (type) => {
    if (type === 'critical') setText("Building collapsed on 1200 Westheimer Rd. We have about 10 people trapped. Need rescue teams urgently!");
    if (type === 'high') setText("Water lines are down in the whole neighborhood near Memorial Park. Hundreds of people without clean water. Please help.");
  };

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
      <div className="bg-bg-surface border border-border-subtle w-full max-w-md rounded-[2px] shadow-2xl overflow-hidden flex flex-col">
        <div className="h-10 border-b border-border-subtle flex items-center justify-between px-4 bg-bg-elevated">
          <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
            Simulate Incoming Report
          </span>
          <button onClick={onClose} className="text-text-muted hover:text-text-primary">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 flex flex-col gap-4 text-sm">
          {error && <div className="text-critical text-xs">{error}</div>}
          
          <div className="flex gap-2 mb-2">
            <button type="button" onClick={() => loadPreset('critical')} className="text-[10px] uppercase border border-border-subtle px-2 py-1 text-text-muted hover:text-text-primary">Preset: Rescue</button>
            <button type="button" onClick={() => loadPreset('high')} className="text-[10px] uppercase border border-border-subtle px-2 py-1 text-text-muted hover:text-text-primary">Preset: Water</button>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-text-muted uppercase tracking-wider">Channel</label>
            <select 
              value={channel} 
              onChange={e => setChannel(e.target.value)}
              className="bg-bg-elevated border border-border-subtle text-text-primary p-2 text-sm rounded-[2px] focus:outline-none focus:border-accent"
            >
              <option value="sms">SMS</option>
              <option value="web_form">Web Form</option>
              <option value="twitter">Social Media</option>
            </select>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-text-muted uppercase tracking-wider">Raw Text</label>
            <textarea 
              value={text}
              onChange={e => setText(e.target.value)}
              required
              rows={4}
              className="bg-bg-elevated border border-border-subtle text-text-primary p-2 text-sm rounded-[2px] focus:outline-none focus:border-accent resize-none"
              placeholder="Enter incident description..."
            />
          </div>

          <div className="pt-2 flex justify-end">
            <button 
              type="submit"
              disabled={loading || !text.trim()}
              className="text-xs uppercase tracking-wider font-semibold bg-accent hover:bg-blue-400 text-white px-6 py-2 rounded-[2px] transition-colors disabled:opacity-50"
            >
              {loading ? 'Submitting...' : 'Ingest Report'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReportModal;
