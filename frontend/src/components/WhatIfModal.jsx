import React, { useState } from 'react';
import { X, Sliders, Zap, CheckCircle2, RotateCcw, ArrowRight } from 'lucide-react';

export default function WhatIfModal({ isOpen, onClose, currentWeights, currentImportances, onApply }) {
  if (!isOpen) return null;

  const [weights, setWeights] = useState({
    technical_skills: currentWeights?.technical_skills || 35.0,
    experience: currentWeights?.experience || 20.0,
    projects: currentWeights?.projects || 15.0,
    required_skills: currentWeights?.required_skills || 10.0,
    education: currentWeights?.education || 10.0,
    preferred_skills: currentWeights?.preferred_skills || 5.0,
    achievements: currentWeights?.achievements || 5.0,
  });

  const [importances, setImportances] = useState({
    Java: currentImportances?.Java || 'critical',
    'Spring Boot': currentImportances?.['Spring Boot'] || 'critical',
    SQL: currentImportances?.SQL || 'important',
    'REST APIs': currentImportances?.['REST APIs'] || 'important',
    AWS: currentImportances?.AWS || 'preferred',
    Docker: currentImportances?.Docker || 'preferred',
  });

  const totalWeight = Object.values(weights).reduce((a, b) => a + Number(b), 0);

  const handleSliderChange = (key, value) => {
    setWeights(prev => ({
      ...prev,
      [key]: parseFloat(value)
    }));
  };

  const handleImportanceToggle = (skill, val) => {
    setImportances(prev => ({
      ...prev,
      [skill]: val
    }));
  };

  // Preset scenarios
  const applyPreset = (type) => {
    if (type === 'default') {
      setWeights({
        technical_skills: 35.0,
        experience: 20.0,
        projects: 15.0,
        required_skills: 10.0,
        education: 10.0,
        preferred_skills: 5.0,
        achievements: 5.0,
      });
      setImportances({
        Java: 'critical',
        'Spring Boot': 'critical',
        SQL: 'important',
        'REST APIs': 'important',
        AWS: 'preferred',
        Docker: 'preferred',
      });
    } else if (type === 'aws_cloud') {
      // Demo scenario prompt 11 & 47: Increase AWS importance & weight
      setWeights({
        technical_skills: 30.0,
        experience: 20.0,
        projects: 15.0,
        required_skills: 10.0,
        education: 5.0,
        preferred_skills: 15.0,
        achievements: 5.0,
      });
      setImportances({
        Java: 'critical',
        'Spring Boot': 'important',
        SQL: 'important',
        'REST APIs': 'important',
        AWS: 'critical',
        Docker: 'important',
      });
    } else if (type === 'fresher') {
      setWeights({
        technical_skills: 40.0,
        experience: 5.0,
        projects: 25.0,
        required_skills: 15.0,
        education: 10.0,
        preferred_skills: 2.0,
        achievements: 3.0,
      });
      setImportances({
        Java: 'critical',
        'Spring Boot': 'important',
        SQL: 'important',
        'REST APIs': 'important',
        AWS: 'preferred',
        Docker: 'preferred',
      });
    }
  };

  const handleSimulate = () => {
    onApply(weights, importances);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '780px', padding: '28px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              background: 'rgba(99, 102, 241, 0.2)',
              border: '1px solid rgba(99, 102, 241, 0.4)',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Sliders size={20} color="#818cf8" />
            </div>
            <div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>What-If Hiring Simulator</h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                Dynamically adjust scoring weights and requirement importance to simulate ranking shifts.
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Preset Pills */}
        <div style={{ marginBottom: '22px' }}>
          <label style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', display: 'block', marginBottom: '8px' }}>
            Quick Simulation Scenarios
          </label>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => applyPreset('default')}
            >
              <RotateCcw size={14} />
              <span>Standard Enterprise (Default)</span>
            </button>
            <button 
              className="btn btn-outline-primary btn-sm"
              onClick={() => applyPreset('aws_cloud')}
              style={{ background: 'rgba(99, 102, 241, 0.12)', borderColor: '#818cf8', color: '#ffffff' }}
            >
              <Zap size={14} color="#f59e0b" />
              <span>Cloud First (AWS → Critical, Pref → 15%)</span>
            </button>
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => applyPreset('fresher')}
            >
              <CheckCircle2 size={14} />
              <span>Project & Algorithmic Heavy</span>
            </button>
          </div>
        </div>

        {/* Two Column Layout */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          {/* Column 1: Component Weights */}
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>Scoring Component Weights</span>
              <span className={`badge ${Math.round(totalWeight) === 100 ? 'badge-strong' : 'badge-weak'}`} style={{ fontSize: '0.75rem' }}>
                Total: {Math.round(totalWeight)}%
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {[
                { key: 'technical_skills', label: 'Technical Skills', max: 60 },
                { key: 'experience', label: 'Work Experience', max: 50 },
                { key: 'projects', label: 'Projects Depth', max: 40 },
                { key: 'required_skills', label: 'Critical Requirements', max: 30 },
                { key: 'education', label: 'Education Degree', max: 30 },
                { key: 'preferred_skills', label: 'Preferred / Cloud', max: 30 },
                { key: 'achievements', label: 'Certifications & Awards', max: 20 },
              ].map(item => (
                <div key={item.key}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
                    <span style={{ color: '#cbd5e1' }}>{item.label}</span>
                    <span style={{ fontWeight: 700, color: '#818cf8', fontFamily: 'var(--font-mono)' }}>
                      {weights[item.key]}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max={item.max}
                    step="1"
                    value={weights[item.key]}
                    onChange={(e) => handleSliderChange(item.key, e.target.value)}
                    style={{ width: '100%', accentColor: '#6366f1', cursor: 'pointer' }}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Column 2: Requirement Importance Toggles */}
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, display: 'block', marginBottom: '14px' }}>
              Requirement Importance Classification
            </span>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {[
                { name: 'Java', key: 'Java' },
                { name: 'Spring Boot', key: 'Spring Boot' },
                { name: 'SQL', key: 'SQL' },
                { name: 'REST APIs', key: 'REST APIs' },
                { name: 'AWS (Cloud)', key: 'AWS' },
                { name: 'Docker', key: 'Docker' },
              ].map(skill => {
                const currentImp = importances[skill.key] || 'important';
                return (
                  <div key={skill.key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                    <span style={{ fontSize: '0.825rem', fontWeight: 600, color: '#e2e8f0' }}>{skill.name}</span>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      {['critical', 'important', 'preferred'].map(level => (
                        <button
                          key={level}
                          type="button"
                          onClick={() => handleImportanceToggle(skill.key, level)}
                          style={{
                            padding: '3px 8px',
                            fontSize: '0.7rem',
                            fontWeight: 600,
                            borderRadius: '4px',
                            border: '1px solid',
                            cursor: 'pointer',
                            background: currentImp === level ? (
                              level === 'critical' ? 'rgba(239, 68, 68, 0.25)' :
                              level === 'important' ? 'rgba(245, 158, 11, 0.25)' : 'rgba(99, 102, 241, 0.25)'
                            ) : 'transparent',
                            borderColor: currentImp === level ? (
                              level === 'critical' ? '#ef4444' :
                              level === 'important' ? '#f59e0b' : '#6366f1'
                            ) : 'rgba(255,255,255,0.1)',
                            color: currentImp === level ? '#ffffff' : '#94a3b8'
                          }}
                        >
                          {level.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            <div style={{ marginTop: '16px', padding: '10px 12px', background: 'rgba(99, 102, 241, 0.08)', borderRadius: '8px', border: '1px solid rgba(99, 102, 241, 0.2)', fontSize: '0.75rem', color: '#cbd5e1' }}>
              <strong>Demo Tip:</strong> Switch <em>AWS (Cloud)</em> from <strong>PREFERRED</strong> to <strong>CRITICAL</strong> to observe Candidate #14 overtake Candidate #07 for the #1 rank with explainable cause!
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={handleSimulate}>
            <Zap size={16} />
            <span>Simulate & Recalculate Rankings</span>
          </button>
        </div>
      </div>
    </div>
  );
}
