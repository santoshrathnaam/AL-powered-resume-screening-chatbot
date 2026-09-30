import React, { useState, useEffect } from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  Award, 
  CheckCircle, 
  AlertTriangle, 
  AlertCircle, 
  HelpCircle, 
  ShieldCheck, 
  Briefcase, 
  GraduationCap, 
  Code, 
  FileCheck2, 
  Sparkles, 
  Layers, 
  Activity, 
  MessageSquareCode,
  Scale,
  User,
  Users,
  Plus,
  Trash2,
  Zap,
  ArrowRight,
  Shuffle
} from 'lucide-react';

export default function CandidateDetailPage({ 
  candidateId, 
  allCandidates, 
  onSelectCandidate, 
  anonymize 
}) {
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('skills'); // 'skills' | 'explainability' | 'claims_risks' | 'interview'
  
  // Comparison state (2 to 3 candidates)
  const [viewMode, setViewMode] = useState('single'); // 'single' | 'compare'
  const [compareIds, setCompareIds] = useState(['Candidate #07', 'Candidate #14']);
  const [comparisonData, setComparisonData] = useState(null);
  const [compareLoading, setCompareLoading] = useState(false);

  useEffect(() => {
    if (candidateId) {
      fetchCandidate(candidateId);
      // Ensure the active candidate is included in comparison
      if (!compareIds.includes(candidateId)) {
        setCompareIds([candidateId, compareIds[0] || 'Candidate #14'].slice(0, 3));
      }
    }
  }, [candidateId]);

  useEffect(() => {
    if (viewMode === 'compare' && compareIds.length >= 2) {
      fetchComparison(compareIds);
    }
  }, [viewMode, compareIds]);

  const fetchCandidate = async (cid) => {
    let targetId = cid;
    if (!targetId || targetId.trim() === 'Candidate' || targetId.trim() === '') {
      if (allCandidates && allCandidates.length > 0) {
        targetId = allCandidates[0].candidate_id;
      } else {
        return;
      }
    }
    setLoading(true);
    try {
      const res = await fetch(`/api/candidate/${encodeURIComponent(targetId)}`);
      if (res.ok) {
        const json = await res.json();
        setCandidate(json);
      }
    } catch (e) {
      console.error("Failed to load candidate:", e);
    } finally {
      setLoading(false);
    }
  };

  const fetchComparison = async (ids) => {
    setCompareLoading(true);
    try {
      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ candidate_ids: ids })
      });
      if (res.ok) {
        const json = await res.json();
        setComparisonData(json);
      }
    } catch (e) {
      console.error("Failed to load comparison:", e);
    } finally {
      setCompareLoading(false);
    }
  };

  const handleAddCandidateToCompare = (newId) => {
    if (compareIds.length < 3 && !compareIds.includes(newId)) {
      const updated = [...compareIds, newId];
      setCompareIds(updated);
    }
  };

  const handleRemoveCompareCandidate = (idToRemove) => {
    if (compareIds.length > 2) {
      const updated = compareIds.filter(id => id !== idToRemove);
      setCompareIds(updated);
    }
  };

  const handleSelectCompareCandidate = (index, newId) => {
    const updated = [...compareIds];
    updated[index] = newId;
    setCompareIds(updated);
  };

  const handleRandomCompare = (count = 2) => {
    if (!allCandidates || allCandidates.length < 2) return;
    const shuffled = [...allCandidates].sort(() => 0.5 - Math.random());
    const picked = shuffled.slice(0, Math.min(count, shuffled.length)).map(c => c.candidate_id);
    setCompareIds(picked);
    setViewMode('compare');
  };

  const formatCandidateDisplayName = (c) => {
    if (!c) return '';
    if (anonymize) return c.anonymized_id;
    if (c.profile?.raw_name && c.profile.raw_name !== "Applicant") {
      return `${c.candidate_id} • ${c.profile.raw_name}`;
    }
    return c.candidate_id;
  };

  if (!candidate && allCandidates.length > 0) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: '#94a3b8' }}>
        Loading candidate intelligence...
      </div>
    );
  }

  // Find index for prev/next navigation
  const currentIndex = allCandidates.findIndex(c => c.candidate_id === candidate?.candidate_id);
  const prevCandidate = currentIndex > 0 ? allCandidates[currentIndex - 1] : null;
  const nextCandidate = currentIndex < allCandidates.length - 1 ? allCandidates[currentIndex + 1] : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* MODE TOGGLE BAR: SINGLE PROFILE vs COMPARE 2-3 CANDIDATES */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        background: 'rgba(15, 23, 42, 0.65)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '12px',
        padding: '10px 18px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            className={`btn btn-sm ${viewMode === 'single' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setViewMode('single')}
          >
            <User size={15} />
            <span>Individual Deep Dive</span>
          </button>

          <button
            className={`btn btn-sm ${viewMode === 'compare' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => {
              setViewMode('compare');
              if (compareIds.length < 2) {
                const second = allCandidates.find(c => c.candidate_id !== candidate?.candidate_id)?.candidate_id || 'Candidate #14';
                setCompareIds([candidate?.candidate_id || 'Candidate #07', second]);
              }
            }}
          >
            <Scale size={15} />
            <span>Compare 2–3 Candidates ({compareIds.length} Selected)</span>
          </button>
        </div>

        {viewMode === 'single' ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => handleRandomCompare(2)}
              title="Randomly pick 2 candidates to compare"
            >
              <Shuffle size={14} color="#818cf8" />
              <span>Random 2</span>
            </button>
            {allCandidates.length >= 3 && (
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => handleRandomCompare(3)}
                title="Randomly pick 3 candidates to compare"
              >
                <Shuffle size={14} color="#34d399" />
                <span>Random 3</span>
              </button>
            )}
            <button
              className="btn btn-outline-primary btn-sm"
              onClick={() => {
                const other = allCandidates.find(c => c.candidate_id !== candidate?.candidate_id)?.candidate_id || 'Candidate #14';
                setCompareIds([candidate?.candidate_id || 'Candidate #07', other]);
                setViewMode('compare');
              }}
            >
              <Scale size={14} />
              <span>Compare {candidate?.candidate_id}</span>
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: '#94a3b8' }}>
            <span>Comparison Matrix: <strong>{compareIds.length} Candidates</strong> (Max 3)</span>
          </div>
        )}
      </div>

      {/* ========================================================================= */}
      {/* VIEW MODE 1: SINGLE CANDIDATE PROFILE DEEP DIVE                           */}
      {/* ========================================================================= */}
      {viewMode === 'single' && candidate && (
        <>
          {/* CANDIDATE HEADER */}
          <div className="glass-panel" style={{ padding: '24px 28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '20px' }}>
              {/* Quick Switch Dropdown */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '0.8rem', color: '#94a3b8', fontWeight: 600 }}>Active Candidate:</span>
                <select
                  className="select-control"
                  value={candidate.candidate_id}
                  onChange={(e) => onSelectCandidate(e.target.value)}
                  style={{ width: '260px', fontWeight: 700 }}
                >
                  {allCandidates.map(c => (
                    <option key={c.candidate_id} value={c.candidate_id}>
                      #{c.rank} {formatCandidateDisplayName(c)} ({c.overall_score}%)
                    </option>
                  ))}
                </select>
              </div>

              {/* Prev / Next buttons */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  className="btn btn-secondary btn-sm"
                  disabled={!prevCandidate}
                  onClick={() => prevCandidate && onSelectCandidate(prevCandidate.candidate_id)}
                >
                  <ChevronLeft size={16} />
                  <span>Previous</span>
                </button>
                <button
                  className="btn btn-secondary btn-sm"
                  disabled={!nextCandidate}
                  onClick={() => nextCandidate && onSelectCandidate(nextCandidate.candidate_id)}
                >
                  <span>Next</span>
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>

            {/* Profile Card Main */}
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                  <span style={{
                    background: candidate.rank === 1 ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : '#334155',
                    color: '#ffffff',
                    fontWeight: 800,
                    fontSize: '0.85rem',
                    padding: '4px 10px',
                    borderRadius: '6px'
                  }}>
                    Rank #{candidate.rank}
                  </span>

                  <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#f8fafc' }}>
                    {formatCandidateDisplayName(candidate)}
                  </h1>

                  <span className={`badge ${candidate.category === 'Strong Fit' ? 'pill-fit-strong' : (candidate.category === 'Potential Fit' ? 'pill-fit-potential' : 'pill-fit-gap')}`}>
                    {candidate.category}
                  </span>
                </div>

                <div style={{ display: 'flex', gap: '16px', fontSize: '0.8rem', color: '#94a3b8', flexWrap: 'wrap' }}>
                  <span>Experience: <strong style={{ color: '#f8fafc' }}>{candidate.profile?.total_experience_years || 2.0} Years</strong></span>
                  <span>•</span>
                  <span>Degree: <strong style={{ color: '#f8fafc' }}>{candidate.profile?.education?.[0]?.degree || "B.S. in Computer Science"}</strong></span>
                  <span>•</span>
                  <span>Anonymized ID: <strong style={{ color: '#818cf8', fontFamily: 'var(--font-mono)' }}>{candidate.anonymized_id}</strong></span>
                </div>
              </div>

              {/* Overall Match Gauge Card */}
              <div style={{
                background: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(255,255,255,0.08)',
                padding: '14px 24px',
                borderRadius: '12px',
                textAlign: 'center',
                minWidth: '160px'
              }}>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', fontWeight: 700 }}>
                  Overall Match
                </span>
                <div style={{ fontSize: '2.2rem', fontWeight: 800, color: candidate.rank === 1 ? '#34d399' : '#818cf8', fontFamily: 'var(--font-mono)', lineHeight: 1.1 }}>
                  {candidate.overall_score}%
                </div>
                <span style={{ fontSize: '0.72rem', color: '#10b981', fontWeight: 600 }}>
                  Traceable Score Index
                </span>
              </div>
            </div>

            {/* Traceable Score Breakdown Grid */}
            <div style={{ marginTop: '22px', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '18px' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#94a3b8', display: 'block', marginBottom: '10px' }}>
                Traceable Score Component Breakdown:
              </span>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px' }}>
                {[
                  { label: 'Technical Skills', val: candidate.score_breakdown.technical_skills, max: candidate.score_breakdown.weights_used?.technical_skills || 35 },
                  { label: 'Work Experience', val: candidate.score_breakdown.experience, max: candidate.score_breakdown.weights_used?.experience || 20 },
                  { label: 'Project Depth', val: candidate.score_breakdown.projects, max: candidate.score_breakdown.weights_used?.projects || 15 },
                  { label: 'Critical Req', val: candidate.score_breakdown.required_skills, max: candidate.score_breakdown.weights_used?.required_skills || 10 },
                  { label: 'Education', val: candidate.score_breakdown.education, max: candidate.score_breakdown.weights_used?.education || 10 },
                  { label: 'Preferred / Cloud', val: candidate.score_breakdown.preferred_skills, max: candidate.score_breakdown.weights_used?.preferred_skills || 5 },
                  { label: 'Achievements', val: candidate.score_breakdown.achievements, max: candidate.score_breakdown.weights_used?.achievements || 5 },
                ].map(item => (
                  <div key={item.label} style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'block' }}>{item.label}</span>
                    <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc', fontFamily: 'var(--font-mono)' }}>
                      {item.val} <span style={{ fontSize: '0.75rem', color: '#64748b' }}>/ {item.max}</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* NAVIGATION TABS FOR INTELLIGENCE PANELS */}
          <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '10px', flexWrap: 'wrap' }}>
            {[
              { key: 'skills', label: 'Skill Match & Evidence', icon: Code },
              { key: 'explainability', label: 'Explainability ("Why this candidate?")', icon: Sparkles },
              { key: 'claims_risks', label: 'Claim Verification & Risk Detector', icon: ShieldCheck },
              { key: 'interview', label: 'Interview Readiness & Questions', icon: MessageSquareCode },
            ].map(tab => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.key;
              return (
                <button
                  key={tab.key}
                  className={`btn btn-sm ${isActive ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => setActiveTab(tab.key)}
                >
                  <Icon size={15} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* TAB 1: SKILL MATCH & EVIDENCE EXTRACTION */}
          {activeTab === 'skills' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {/* Skill Gap Summary Row */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
                <div className="glass-panel" style={{ padding: '18px', borderLeft: '4px solid #10b981' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#34d399', display: 'block', marginBottom: '6px' }}>
                    Strong Skills Verified
                  </span>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {candidate.skill_matches.filter(m => m.match_level === 'Strong').map(m => (
                      <span key={m.skill} className="badge badge-strong">{m.skill}</span>
                    ))}
                  </div>
                </div>

                <div className="glass-panel" style={{ padding: '18px', borderLeft: '4px solid #3b82f6' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#60a5fa', display: 'block', marginBottom: '6px' }}>
                    Partial / Adjacent Skills
                  </span>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {candidate.skill_matches.filter(m => m.match_level === 'Partial').map(m => (
                      <span key={m.skill} className="badge badge-partial">{m.skill}</span>
                    ))}
                    {candidate.skill_matches.filter(m => m.match_level === 'Partial').length === 0 && (
                      <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>None identified</span>
                    )}
                  </div>
                </div>

                <div className="glass-panel" style={{ padding: '18px', borderLeft: '4px solid #ef4444' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#f87171', display: 'block', marginBottom: '6px' }}>
                    Missing Requirements (Skill Gap)
                  </span>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {candidate.missing_skills.map((s, idx) => (
                      <span key={idx} className="badge badge-missing">{s}</span>
                    ))}
                    {candidate.missing_skills.length === 0 && (
                      <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Zero critical skills missing</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Detailed Evidence Cards */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '6px' }}>
                  Evidence-Based Skill Analysis
                </h3>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '18px' }}>
                  Every evaluation matches concrete citations from the resume's projects, experience, or certifications.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {candidate.skill_matches.map(m => {
                    const isStrong = m.match_level === 'Strong';
                    const isPartial = m.match_level === 'Partial';
                    const isMissing = m.match_level === 'Missing';

                    return (
                      <div 
                        key={m.skill} 
                        style={{
                          background: 'rgba(255,255,255,0.02)',
                          border: '1px solid rgba(255,255,255,0.06)',
                          borderRadius: '10px',
                          padding: '16px'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <span style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
                              {m.skill}
                            </span>
                            <span className={`badge ${isStrong ? 'badge-strong' : (isPartial ? 'badge-partial' : (isMissing ? 'badge-missing' : 'badge-weak'))}`}>
                              {m.match_level} Match
                            </span>
                            <span className="badge badge-preferred" style={{ fontSize: '0.68rem' }}>
                              {m.importance.toUpperCase()}
                            </span>
                          </div>

                          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                              Confidence: <strong style={{ color: '#f8fafc' }}>{Math.round(m.confidence)}%</strong>
                            </span>
                            {m.evidence_source && (
                              <span className="badge badge-secondary" style={{ fontSize: '0.7rem' }}>
                                Source: {m.evidence_source}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Evidence Snippet */}
                        <div style={{ background: 'rgba(0,0,0,0.25)', padding: '10px 14px', borderRadius: '6px', borderLeft: `3px solid ${isStrong ? '#10b981' : (isPartial ? '#3b82f6' : '#ef4444')}`, margin: '8px 0', fontSize: '0.8rem', color: '#cbd5e1', fontStyle: 'italic' }}>
                          "{m.evidence_snippet}"
                        </div>

                        {/* AI Assessment Note */}
                        {m.note && (
                          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>
                            <strong>AI Assessment:</strong> {m.note}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: EXPLAINABLE AI */}
          {activeTab === 'explainability' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                <div className="glass-panel" style={{ padding: '24px', borderTop: '4px solid #10b981' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                    <Sparkles size={20} color="#34d399" />
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                      Why Rank #{candidate.rank}? (Strengths & Rationale)
                    </h3>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {candidate.why_this_candidate.map((reason, idx) => (
                      <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.825rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                        <CheckCircle size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                        <span>{reason}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="glass-panel" style={{ padding: '24px', borderTop: '4px solid #f59e0b' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                    <HelpCircle size={20} color="#fbbf24" />
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                      Why Not Ranked Higher? (Gap Analysis)
                    </h3>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {candidate.why_not_higher.map((reason, idx) => (
                      <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.825rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                        <AlertCircle size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: '2px' }} />
                        <span>{reason}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Resume Projects Reference */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '14px' }}>
                  Documented Technical Projects
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
                  {candidate.profile?.projects?.map((p, idx) => (
                    <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
                      <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '6px' }}>
                        {p.title}
                      </h4>
                      <p style={{ fontSize: '0.8rem', color: '#cbd5e1', lineHeight: '1.5', marginBottom: '10px' }}>
                        {p.description}
                      </p>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {p.technologies?.map(tech => (
                          <span key={tech} className="badge badge-secondary" style={{ fontSize: '0.7rem' }}>
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: CLAIM VERIFICATION & RISKS */}
          {activeTab === 'claims_risks' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div className="glass-panel" style={{ padding: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                  <FileCheck2 size={20} color="#818cf8" />
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                    Resume Claim vs. Evidence Verification
                  </h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '18px' }}>
                  Detects potentially unsupported assertions or skills claiming expertise without verified production depth.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {candidate.claims.map((c, idx) => (
                    <div key={idx} style={{
                      background: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(255,255,255,0.06)',
                      borderRadius: '10px',
                      padding: '16px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc' }}>
                          Claim: {c.claim}
                        </span>
                        <span className={`badge ${c.status === 'Verified' ? 'badge-strong' : 'badge-weak'}`}>
                          {c.status}
                        </span>
                      </div>

                      <p style={{ fontSize: '0.8rem', color: '#cbd5e1', marginBottom: '6px' }}>
                        <strong>Evidence Found:</strong> {c.evidence_found}
                      </p>
                      <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        <strong>Interview Recommendation:</strong> {c.recommendation}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                  <AlertTriangle size={20} color="#f59e0b" />
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                    Resume Consistency & Anomaly Detector
                  </h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '18px' }}>
                  Identifies timeline overlaps, unexplained intervals, or vague technical contributions.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {candidate.risks.map((r, idx) => (
                    <div key={idx} style={{
                      background: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(255,255,255,0.06)',
                      borderRadius: '10px',
                      padding: '16px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc' }}>
                          {r.title}
                        </span>
                        <span className={`badge ${r.severity === 'High' ? 'badge-missing' : (r.severity === 'Medium' ? 'badge-weak' : 'badge-secondary')}`}>
                          {r.severity} Severity
                        </span>
                      </div>
                      <p style={{ fontSize: '0.8rem', color: '#cbd5e1', marginBottom: '6px' }}>
                        {r.description}
                      </p>
                      <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        <strong>Action:</strong> {r.recommendation}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: INTERVIEW READINESS & QUESTIONS */}
          {activeTab === 'interview' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div className="glass-panel" style={{ padding: '24px', borderLeft: '4px solid #8b5cf6' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '16px' }}>
                  <div>
                    <span className="badge badge-preferred" style={{ marginBottom: '6px' }}>
                      Interview Readiness Assessment
                    </span>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                      Readiness Level: <span style={{ color: '#34d399' }}>{candidate.interview_readiness.overall_readiness}</span>
                    </h3>
                  </div>

                  <div style={{ display: 'flex', gap: '16px', textAlign: 'center' }}>
                    <div>
                      <span style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'block' }}>Technical Strength</span>
                      <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc', fontFamily: 'var(--font-mono)' }}>
                        {candidate.interview_readiness.technical_strength}%
                      </span>
                    </div>
                    <div>
                      <span style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'block' }}>Experience Fit</span>
                      <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc', fontFamily: 'var(--font-mono)' }}>
                        {candidate.interview_readiness.experience_fit}%
                      </span>
                    </div>
                    <div>
                      <span style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'block' }}>Evidence Confidence</span>
                      <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#34d399', fontFamily: 'var(--font-mono)' }}>
                        {candidate.interview_readiness.evidence_confidence}%
                      </span>
                    </div>
                  </div>
                </div>

                <p style={{ fontSize: '0.825rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                  {candidate.interview_readiness.explanation}
                </p>
              </div>

              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '6px' }}>
                  Personalized & Evidence-Grounded Interview Questions
                </h3>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '20px' }}>
                  Questions dynamically synthesized to probe critical claims, architectural decisions, and verification gaps.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {candidate.interview_questions.map((q) => {
                    const isHigh = q.priority === 'High';
                    return (
                      <div 
                        key={q.id}
                        style={{
                          background: 'rgba(255,255,255,0.02)',
                          border: '1px solid rgba(255,255,255,0.06)',
                          borderRadius: '10px',
                          padding: '18px'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{
                              background: isHigh ? 'rgba(239, 68, 68, 0.2)' : 'rgba(59, 130, 246, 0.2)',
                              color: isHigh ? '#f87171' : '#60a5fa',
                              fontSize: '0.7rem',
                              fontWeight: 700,
                              padding: '3px 8px',
                              borderRadius: '4px',
                              border: `1px solid ${isHigh ? 'rgba(239, 68, 68, 0.4)' : 'rgba(59, 130, 246, 0.4)'}`
                            }}>
                              {q.priority.toUpperCase()} PRIORITY
                            </span>
                            <span className="badge badge-secondary" style={{ fontSize: '0.7rem' }}>
                              Category: {q.category}
                            </span>
                          </div>
                          <span style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                            {q.id}
                          </span>
                        </div>

                        <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc', marginBottom: '8px', lineHeight: '1.5' }}>
                          "{q.question}"
                        </h4>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '0.78rem', color: '#94a3b8' }}>
                          <p>
                            <strong style={{ color: '#cbd5e1' }}>Why Ask:</strong> {q.context_reason}
                          </p>
                          <p>
                            <strong style={{ color: '#cbd5e1' }}>What to Look For:</strong> {q.suggested_evaluation}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* ========================================================================= */}
      {/* VIEW MODE 2: INTERACTIVE 2 TO 3 CANDIDATE COMPARISON MATRIX              */}
      {/* ========================================================================= */}
      {viewMode === 'compare' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* COMPARISON CANDIDATE SELECTOR PANEL */}
          <div className="glass-panel" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px', marginBottom: '18px' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Scale size={20} color="#818cf8" />
                  <span>Interactive Multi-Candidate Comparison</span>
                  <span className="badge badge-preferred">{compareIds.length} of 3 Candidates</span>
                </h3>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                  Select 2 or 3 candidates from your pool to compare qualifications, skill evidence, and hiring trade-offs side-by-side.
                </p>
              </div>

              {/* Quick Presets */}
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => handleRandomCompare(2)}
                  title="Randomly pick 2 candidates from active pool"
                >
                  <Shuffle size={14} color="#818cf8" />
                  <span>Random 2</span>
                </button>

                {allCandidates.length >= 3 && (
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => handleRandomCompare(3)}
                    title="Randomly pick 3 candidates from active pool"
                  >
                    <Shuffle size={14} color="#34d399" />
                    <span>Random 3</span>
                  </button>
                )}

                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => {
                    const top2 = allCandidates.slice(0, 2).map(c => c.candidate_id);
                    setCompareIds(top2);
                  }}
                >
                  <Zap size={14} color="#f59e0b" />
                  <span>Top 2 (#1 vs #2)</span>
                </button>

                {allCandidates.length >= 3 && (
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => {
                      const top3 = allCandidates.slice(0, 3).map(c => c.candidate_id);
                      setCompareIds(top3);
                    }}
                  >
                    <Users size={14} color="#38bdf8" />
                    <span>Top 3 (#1 vs #2 vs #3)</span>
                  </button>
                )}
              </div>
            </div>

            {/* Candidate Dropdown Selectors Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: `repeat(${compareIds.length >= 3 ? 3 : 2}, 1fr)`, gap: '16px' }}>
              {compareIds.map((cid, slotIdx) => {
                const currentCand = allCandidates.find(c => c.candidate_id === cid || c.anonymized_id === cid);
                return (
                  <div 
                    key={slotIdx}
                    style={{
                      background: 'rgba(255, 255, 255, 0.02)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      borderRadius: '10px',
                      padding: '14px'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase' }}>
                        Candidate Slot #{slotIdx + 1}
                      </span>
                      {compareIds.length > 2 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveCompareCandidate(cid)}
                          style={{ background: 'transparent', border: 'none', color: '#f87171', cursor: 'pointer', padding: '2px' }}
                          title="Remove from comparison"
                        >
                          <Trash2 size={14} />
                        </button>
                      )}
                    </div>

                    <select
                      className="select-control"
                      value={cid}
                      onChange={(e) => handleSelectCompareCandidate(slotIdx, e.target.value)}
                      style={{ fontWeight: 700, marginBottom: '8px' }}
                    >
                      {allCandidates.map(c => (
                        <option key={c.candidate_id} value={c.candidate_id}>
                          #{c.rank} {formatCandidateDisplayName(c)} ({c.overall_score}%)
                        </option>
                      ))}
                    </select>

                    {currentCand && (
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8' }}>
                        <span>Score: <strong style={{ color: '#34d399' }}>{currentCand.overall_score}%</strong></span>
                        <span>{currentCand.category}</span>
                        <span>{currentCand.profile?.total_experience_years || 2.0} yrs</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Add 3rd Candidate button */}
            {compareIds.length < 3 && allCandidates.length >= 3 && (
              <div style={{ marginTop: '14px', textAlign: 'center' }}>
                <button
                  type="button"
                  className="btn btn-outline-primary btn-sm"
                  onClick={() => {
                    const unused = allCandidates.find(c => !compareIds.includes(c.candidate_id));
                    if (unused) {
                      handleAddCandidateToCompare(unused.candidate_id);
                    }
                  }}
                >
                  <Plus size={15} />
                  <span>Add 3rd Candidate to Comparison</span>
                </button>
              </div>
            )}
          </div>

          {/* SIDE-BY-SIDE EXECUTIVE SCORECARDS */}
          {compareLoading ? (
            <div className="glass-panel" style={{ padding: '50px', textAlign: 'center', color: '#94a3b8' }}>
              Synthesizing multi-candidate comparative metrics...
            </div>
          ) : comparisonData ? (
            <>
              {/* Executive Cards Row */}
              <div style={{ display: 'grid', gridTemplateColumns: `repeat(${comparisonData.candidates.length}, 1fr)`, gap: '18px' }}>
                {comparisonData.candidates.map((c) => {
                  const isWinner = c.rank === Math.min(...comparisonData.candidates.map(x => x.rank));
                  return (
                    <div 
                      key={c.candidate_id}
                      className={`glass-panel ${isWinner ? 'top-rank-glow' : ''}`}
                      style={{
                        padding: '20px',
                        border: isWinner ? '1px solid #10b981' : '1px solid rgba(255, 255, 255, 0.08)',
                        position: 'relative'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{
                            background: isWinner ? '#10b981' : '#334155',
                            color: '#ffffff',
                            fontWeight: 800,
                            fontSize: '0.8rem',
                            padding: '3px 8px',
                            borderRadius: '6px'
                          }}>
                            Rank #{c.rank}
                          </span>
                          <span style={{ fontSize: '1rem', fontWeight: 800, color: '#f8fafc' }}>
                            {formatCandidateDisplayName(c)}
                          </span>
                        </div>
                        {isWinner && (
                          <span className="badge badge-strong" style={{ fontSize: '0.68rem' }}>
                            Highest Fit
                          </span>
                        )}
                      </div>

                      <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '10px' }}>
                        <span style={{ fontSize: '1.8rem', fontWeight: 800, color: isWinner ? '#34d399' : '#818cf8', fontFamily: 'var(--font-mono)' }}>
                          {c.overall_score}%
                        </span>
                        <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Overall Match</span>
                      </div>

                      <div style={{ display: 'flex', gap: '8px', marginBottom: '14px', flexWrap: 'wrap' }}>
                        <span className={`badge ${c.category === 'Strong Fit' ? 'pill-fit-strong' : 'pill-fit-potential'}`}>
                          {c.category}
                        </span>
                        <span className="badge badge-secondary">
                          {c.profile?.total_experience_years || 2.0} yrs exp
                        </span>
                      </div>

                      <div style={{ fontSize: '0.78rem', color: '#cbd5e1', lineHeight: '1.4', marginBottom: '14px' }}>
                        <strong style={{ color: '#818cf8' }}>Top Strength:</strong> {c.strengths[0]}
                      </div>

                      <button
                        className="btn btn-secondary btn-sm"
                        style={{ width: '100%', fontSize: '0.75rem' }}
                        onClick={() => {
                          onSelectCandidate(c.candidate_id);
                          setViewMode('single');
                        }}
                      >
                        Inspect Full Profile
                      </button>
                    </div>
                  );
                })}
              </div>

              {/* DETAILED SIDE-BY-SIDE MATRIX TABLE */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '6px' }}>
                  Detailed Criteria Comparison Matrix
                </h3>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '18px' }}>
                  Direct evaluation of skills, experience, and projects across the {comparisonData.candidates.length} candidates.
                </p>

                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead>
                      <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                        <th style={{ padding: '12px 16px', fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', width: '22%' }}>Criteria</th>
                        {comparisonData.candidates.map(c => (
                          <th key={c.candidate_id} style={{ padding: '12px 16px', fontSize: '0.85rem', color: '#f8fafc', fontWeight: 800 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <span>{formatCandidateDisplayName(c)}</span>
                              <span className="badge badge-strong" style={{ fontSize: '0.68rem', padding: '2px 6px' }}>
                                #{c.rank} ({c.overall_score}%)
                              </span>
                            </div>
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {comparisonData.matrix.map((row, idx) => (
                        <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)', background: idx % 2 === 0 ? 'rgba(255,255,255,0.01)' : 'transparent' }}>
                          <td style={{ padding: '12px 16px', fontWeight: 700, fontSize: '0.825rem', color: '#cbd5e1' }}>
                            {row.criteria}
                            {row.notes && <span style={{ display: 'block', fontSize: '0.7rem', color: '#64748b', fontWeight: 400 }}>{row.notes}</span>}
                          </td>
                          {comparisonData.candidates.map(c => {
                            const scoreVal = row.scores[c.candidate_id] || "N/A";
                            const isHighest = row.highest_candidate === c.candidate_id;
                            const isStrong = typeof scoreVal === 'string' && scoreVal.includes('Strong');
                            const isMissing = typeof scoreVal === 'string' && scoreVal.includes('Missing');

                            return (
                              <td key={c.candidate_id} style={{ padding: '12px 16px', fontSize: '0.825rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                  <span style={{ 
                                    fontWeight: isHighest ? 700 : 500,
                                    color: isStrong ? '#34d399' : (isMissing ? '#f87171' : '#f8fafc')
                                  }}>
                                    {scoreVal}
                                  </span>
                                  {isHighest && (
                                    <Award size={14} color="#10b981" title="Highest rated in this dimension" />
                                  )}
                                </div>
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* AI COMPARATIVE DIFFERENTIATORS SUMMARY CARD */}
              <div className="glass-panel" style={{ padding: '22px', borderLeft: '4px solid #8b5cf6' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                  <Sparkles size={18} color="#818cf8" />
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#f8fafc' }}>
                    AI Comparative Analysis & Recruiter Guidance
                  </h4>
                </div>
                <p style={{ fontSize: '0.825rem', color: '#cbd5e1', lineHeight: '1.6', marginBottom: '12px' }}>
                  {comparisonData.summary}
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {comparisonData.key_differentiators.map((diff, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.8rem', color: '#94a3b8' }}>
                      <ArrowRight size={14} color="#818cf8" style={{ flexShrink: 0, marginTop: '3px' }} />
                      <span>{diff}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : null}
        </div>
      )}
    </div>
  );
}
