import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await client.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      localStorage.setItem('token', response.data.access_token);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-base flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm flex flex-col gap-6">
        
        <div className="flex flex-col items-center gap-2">
          <h1 className="text-sm font-semibold tracking-widest text-text-primary uppercase">
            Disaster Coordinator
          </h1>
          <span className="text-xs text-text-muted tracking-wider uppercase">System Access</span>
        </div>

        <div className="bg-bg-surface border border-border-subtle p-6 rounded-[2px] shadow-2xl">
          {error && (
            <div className="text-critical text-xs mb-4 text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-semibold text-text-secondary uppercase tracking-wider">Operator ID</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-bg-elevated border border-border-subtle rounded-[2px] px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent transition-colors"
                required
              />
            </div>
            
            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-semibold text-text-secondary uppercase tracking-wider">Passcode</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-bg-elevated border border-border-subtle rounded-[2px] px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent transition-colors"
                required
              />
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-accent hover:bg-blue-400 text-white text-xs font-semibold uppercase tracking-wider py-2.5 mt-2 rounded-[2px] transition-colors disabled:opacity-50"
            >
              {loading ? 'Authenticating...' : 'Initialize Session'}
            </button>
          </form>
        </div>

        <div className="text-center text-[10px] text-text-muted uppercase tracking-widest">
          Demo: alice / reviewer_pass
        </div>
      </div>
    </div>
  );
}