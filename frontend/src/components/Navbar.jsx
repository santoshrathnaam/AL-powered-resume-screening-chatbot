import React from 'react';
import { 
  Sparkles, 
  LayoutDashboard, 
  UserCheck, 
  BotMessageSquare, 
  Sliders, 
  RotateCcw, 
  ShieldCheck, 
  ShieldOff 
} from 'lucide-react';

export default function Navbar({ 
  activePage, 
  setActivePage, 
  onOpenWhatIf, 
  onResetDemo, 
  anonymize, 
  setAnonymize,
  version
}) {
  return (
    <header style={{
      background: 'rgba(11, 15, 25, 0.85)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '0 28px'
    }}>
      <div style={{
        maxWidth: '1440px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '70px',
        gap: '20px'
      }}>
        {/* Brand */}
        <div 
          onClick={() => setActivePage('dashboard')} 
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
        >
          <div style={{
            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 12px rgba(99, 102, 241, 0.4)'
          }}>
            <Sparkles size={22} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em' }} className="title-gradient">
                TalentLens AI
              </span>
              <span className="badge badge-preferred" style={{ fontSize: '0.65rem', padding: '2px 6px' }}>
                v{version}.0
              </span>
            </div>
            <p style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '-2px' }}>
              Explainable AI Recruitment Assistant
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button 
            className={`btn ${activePage === 'dashboard' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActivePage('dashboard')}
          >
            <LayoutDashboard size={17} />
            <span>Dashboard</span>
          </button>

          <button 
            className={`btn ${activePage === 'candidate' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActivePage('candidate')}
          >
            <UserCheck size={17} />
            <span>Candidate Intelligence</span>
          </button>

          <button 
            className={`btn ${activePage === 'chat' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActivePage('chat')}
          >
            <BotMessageSquare size={17} />
            <span>AI Recruiter</span>
          </button>
        </nav>

        {/* Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {/* Bias-Aware Redaction Toggle */}
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => setAnonymize(!anonymize)}
            title={anonymize ? "Bias-Aware Mode Active: Names & Demographics Masked" : "Showing Raw Candidate Details"}
            style={{
              borderColor: anonymize ? 'rgba(16, 185, 129, 0.4)' : 'rgba(255, 255, 255, 0.1)',
              color: anonymize ? '#34d399' : '#94a3b8'
            }}
          >
            {anonymize ? <ShieldCheck size={16} /> : <ShieldOff size={16} />}
            <span>{anonymize ? 'Blind Screening: ON' : 'Blind Screening: OFF'}</span>
          </button>

          {/* What-If Simulator Trigger */}
          <button 
            className="btn btn-outline-primary btn-sm"
            onClick={onOpenWhatIf}
            title="Open What-If Hiring Simulator to adjust criteria weights"
          >
            <Sliders size={16} />
            <span>What-If Simulator</span>
          </button>

          {/* Reset Demo Data Button */}
          <button 
            className="btn btn-secondary btn-sm"
            onClick={onResetDemo}
            title="Reload initial 20 benchmark resumes & Software Engineer JD"
          >
            <RotateCcw size={15} />
            <span>Reset Demo</span>
          </button>
        </div>
      </div>
    </header>
  );
}
