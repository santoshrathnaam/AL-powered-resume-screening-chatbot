import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div style={{
      background: 'linear-gradient(90deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%)',
      borderBottom: '1px solid rgba(99, 102, 241, 0.25)',
      padding: '8px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '10px',
      fontSize: '0.8rem',
      color: '#cbd5e1'
    }}>
      <ShieldAlert size={16} color="#818cf8" style={{ flexShrink: 0 }} />
      <span>
        <strong style={{ color: '#ffffff' }}>HR Decision-Support Disclaimer:</strong> AI-generated rankings and evaluations are decision-support recommendations and must not be used as the sole basis for hiring decisions. Recruiters should independently review candidate information and interview evidence.
      </span>
    </div>
  );
}
