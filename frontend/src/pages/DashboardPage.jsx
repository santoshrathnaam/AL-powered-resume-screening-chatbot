import React, { useState } from 'react';
import { 
  FileText, 
  UploadCloud, 
  Sliders, 
  Search, 
  Scale, 
  CheckCircle2, 
  AlertCircle, 
  TrendingUp, 
  ChevronRight, 
  Sparkles, 
  Award, 
  Users, 
  BarChart3, 
  Layers, 
  Filter,
  Shuffle
} from 'lucide-react';

export default function DashboardPage({ 
  dashboardData, 
  onSelectCandidate, 
  onOpenWhatIf, 
  onOpenJobUpload, 
  onOpenResumeUpload, 
  onOpenComparison,
  selectedForCompare,
  setSelectedForCompare,
  anonymize
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [minExpFilter, setMinExpFilter] = useState(0);

  if (!dashboardData) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0', color: '#94a3b8' }}>
        <p>Initializing TalentLens Screening Engine...</p>
      </div>
    );
  }

  const { job, total_resumes, top_10, all_candidates, statistics, weights } = dashboardData;

  // Filter candidates
  const filteredCandidates = all_candidates.filter(c => {
    const rawName = c.profile?.raw_name || '';
    const idMatch = c.candidate_id.toLowerCase().includes(searchTerm.toLowerCase()) || 
                    c.anonymized_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    rawName.toLowerCase().includes(searchTerm.toLowerCase());
    const skillMatch = c.skill_matches.some(m => m.skill.toLowerCase().includes(searchTerm.toLowerCase()) && m.match_level === 'Strong');
    const matchesSearch = idMatch || skillMatch;
    const matchesCategory = categoryFilter === 'All' || c.category === categoryFilter;
    const matchesExp = (c.profile?.total_experience_years || 0) >= minExpFilter;
    return matchesSearch && matchesCategory && matchesExp;
  });

  const handleCheckboxToggle = (cid) => {
    if (selectedForCompare.includes(cid)) {
      setSelectedForCompare(selectedForCompare.filter(id => id !== cid));
    } else {
      if (selectedForCompare.length < 5) {
        setSelectedForCompare([...selectedForCompare, cid]);
      }
    }
  };

  const formatCandidateDisplayName = (cand) => {
    if (anonymize) return cand.anonymized_id;
    if (cand.profile?.raw_name && cand.profile.raw_name !== "Applicant") {
      return `${cand.candidate_id} • ${cand.profile.raw_name}`;
    }
    return cand.candidate_id;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* SECTION A: JOB DESCRIPTION SUMMARY & CONTROLS */}
      <div className="glass-panel" style={{ padding: '24px 28px', borderLeft: '4px solid #6366f1' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '20px', flexWrap: 'wrap' }}>
          <div style={{ maxWidth: '820px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <span className="badge badge-preferred">Active Job Description</span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>•</span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Min Experience: {job.min_experience_years}+ Years</span>
            </div>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '8px', color: '#f8fafc' }}>
              {job.title}
            </h1>
            <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.6', marginBottom: '16px' }}>
              {job.summary}
            </p>

            {/* Extracted Requirements Categories */}
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#fca5a5', fontWeight: 700, display: 'block', marginBottom: '6px' }}>
                  Critical Requirements:
                </span>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {job.critical_skills.map((s, idx) => (
                    <span key={idx} className="badge badge-critical">{s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#fde68a', fontWeight: 700, display: 'block', marginBottom: '6px' }}>
                  Important Skills:
                </span>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {job.important_skills.map((s, idx) => (
                    <span key={idx} className="badge badge-important">{s}</span>
                  ))}
                </div>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#c7d2fe', fontWeight: 700, display: 'block', marginBottom: '6px' }}>
                  Preferred / Cloud:
                </span>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {job.preferred_skills.map((s, idx) => (
                    <span key={idx} className="badge badge-preferred">{s}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', minWidth: '220px' }}>
            <button className="btn btn-primary" onClick={onOpenResumeUpload}>
              <UploadCloud size={16} />
              <span>Upload Custom Resumes</span>
            </button>
            <button className="btn btn-secondary" onClick={onOpenJobUpload}>
              <FileText size={16} />
              <span>Modify Job Description</span>
            </button>
            <button className="btn btn-outline-primary" onClick={onOpenWhatIf}>
              <Sliders size={16} />
              <span>What-If Simulator</span>
            </button>
          </div>
        </div>
      </div>

      {/* SECTION B: ANALYTICS & STATS CARDS */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Total Resumes</span>
            <Users size={18} color="#818cf8" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc' }}>
            {total_resumes}
          </div>
          <span style={{ fontSize: '0.72rem', color: '#34d399', fontWeight: 600 }}>Screened & Analyzed</span>
        </div>

        <div className="glass-panel" style={{ padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Strong Fit</span>
            <Award size={18} color="#10b981" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#10b981' }}>
            {statistics?.strong_fit || 0}
          </div>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Score ≥ 85%</span>
        </div>

        <div className="glass-panel" style={{ padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Potential Fit</span>
            <Layers size={18} color="#3b82f6" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#3b82f6' }}>
            {statistics?.potential_fit || 0}
          </div>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>70% ≤ Score &lt; 85%</span>
        </div>

        <div className="glass-panel" style={{ padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Skill Gap</span>
            <AlertCircle size={18} color="#f59e0b" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f59e0b' }}>
            {statistics?.skill_gap || 0}
          </div>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>55% ≤ Score &lt; 70%</span>
        </div>

        <div className="glass-panel" style={{ padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Average Match</span>
            <TrendingUp size={18} color="#8b5cf6" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc' }}>
            {statistics?.average_match_score || 78.0}%
          </div>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Pool suitability index</span>
        </div>
      </div>

      {/* SECTION C: INTERACTIVE CHARTS & SKILL COVERAGE */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '20px' }}>
        {/* Skill Coverage Matrix */}
        <div className="glass-panel" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Required Skill Coverage in Candidate Pool</h3>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Candidate proficiency distribution for active JD</p>
            </div>
            <BarChart3 size={18} color="#818cf8" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {job.requirements.slice(0, 6).map((req) => {
              const cov = statistics?.skill_coverage?.[req.skill] || { Strong: 0, Partial: 0, Weak: 0, Missing: 0 };
              const total = total_resumes || 1;
              const pStrong = ((cov.Strong || 0) / total) * 100;
              const pPartial = ((cov.Partial || 0) / total) * 100;
              const pMissing = ((cov.Missing || 0) / total) * 100;

              return (
                <div key={req.skill}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600, color: '#e2e8f0' }}>{req.skill}</span>
                    <span style={{ color: '#94a3b8', fontSize: '0.75rem' }}>
                      {cov.Strong} Strong ({Math.round(pStrong)}%) • {cov.Partial} Partial • {cov.Missing} Missing
                    </span>
                  </div>
                  {/* Multi-segment Progress Bar */}
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '9999px', display: 'flex', overflow: 'hidden' }}>
                    <div style={{ width: `${pStrong}%`, background: '#10b981' }} title={`${cov.Strong} Strong`} />
                    <div style={{ width: `${pPartial}%`, background: '#3b82f6' }} title={`${cov.Partial} Partial`} />
                    <div style={{ width: `${pMissing}%`, background: 'rgba(239, 68, 68, 0.4)' }} title={`${cov.Missing} Missing`} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Candidate Category Distribution */}
        <div className="glass-panel" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Hiring Classification Funnel</h3>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Categorized by multi-criteria explainable index</p>
            </div>
            <Users size={18} color="#10b981" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {statistics?.category_distribution?.map((cat) => {
              const pct = Math.round((cat.count / Math.max(total_resumes || 1, 1)) * 100);
              return (
                <div key={cat.name} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: cat.color }} />
                    <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{cat.name}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc' }}>{cat.count}</span>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8', width: '40px', textAlign: 'right' }}>{pct}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* SECTION D: TOP RANKED CANDIDATES SPOTLIGHT */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>Top Ranked Candidates</span>
              <span className="badge badge-strong">Leaderboard</span>
            </h2>
            <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
              Ranked by evidence-backed multi-criteria scoring against active JD requirements.
            </p>
          </div>
        </div>

        {/* Carousel / Cards grid of Top 3 */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px', marginBottom: '24px' }}>
          {top_10.slice(0, 3).map((cand) => {
            const isRank1 = cand.rank === 1;
            return (
              <div 
                key={cand.candidate_id}
                className={`glass-panel ${isRank1 ? 'top-rank-glow' : ''}`}
                style={{
                  padding: '22px',
                  border: isRank1 ? '1px solid #10b981' : '1px solid rgba(255, 255, 255, 0.08)',
                  position: 'relative',
                  overflow: 'hidden',
                  cursor: 'pointer'
                }}
                onClick={() => onSelectCandidate(cand.candidate_id)}
              >
                {/* Header with Rank & Score */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{
                      background: isRank1 ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'rgba(255,255,255,0.08)',
                      color: '#ffffff',
                      fontWeight: 800,
                      fontSize: '0.85rem',
                      padding: '4px 10px',
                      borderRadius: '6px'
                    }}>
                      #{cand.rank}
                    </span>
                    <span style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc' }}>
                      {formatCandidateDisplayName(cand)}
                    </span>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <span style={{ fontSize: '1.4rem', fontWeight: 800, color: isRank1 ? '#34d399' : '#818cf8', fontFamily: 'var(--font-mono)' }}>
                      {cand.overall_score}%
                    </span>
                    <span style={{ display: 'block', fontSize: '0.68rem', color: '#94a3b8' }}>Match Score</span>
                  </div>
                </div>

                {/* What-If Rank Change Indicator */}
                {cand.rank_change_reason && (
                  <div style={{ marginBottom: '12px', padding: '6px 10px', background: 'rgba(99, 102, 241, 0.12)', borderRadius: '6px', border: '1px solid rgba(99, 102, 241, 0.25)', fontSize: '0.72rem', color: '#c7d2fe' }}>
                    {cand.rank_change_reason}
                  </div>
                )}

                {/* Category Pill */}
                <div style={{ marginBottom: '14px' }}>
                  <span className={`badge ${cand.category === 'Strong Fit' ? 'pill-fit-strong' : (cand.category === 'Potential Fit' ? 'pill-fit-potential' : 'pill-fit-gap')}`}>
                    {cand.category}
                  </span>
                  <span style={{ marginLeft: '8px', fontSize: '0.75rem', color: '#94a3b8' }}>
                    {cand.profile?.total_experience_years || 2.0} yrs exp
                  </span>
                </div>

                {/* Top Strengths */}
                <div style={{ marginBottom: '16px' }}>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: '#94a3b8', display: 'block', marginBottom: '6px' }}>
                    Key Alignment:
                  </span>
                  <p style={{ fontSize: '0.78rem', color: '#cbd5e1', lineHeight: '1.4' }}>
                    {cand.strengths[0] || "Solid technical alignment."}
                  </p>
                </div>

                {/* Skill Badges */}
                <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginBottom: '16px' }}>
                  {cand.skill_matches.slice(0, 4).map(m => (
                    <span 
                      key={m.skill} 
                      className={`badge ${m.match_level === 'Strong' ? 'badge-strong' : (m.match_level === 'Partial' ? 'badge-partial' : 'badge-weak')}`}
                      style={{ fontSize: '0.68rem' }}
                    >
                      {m.skill}: {m.match_level}
                    </span>
                  ))}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '12px' }}>
                  <span style={{ fontSize: '0.75rem', color: '#818cf8', fontWeight: 600 }}>
                    Inspect Candidate Intelligence
                  </span>
                  <ChevronRight size={16} color="#818cf8" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* SECTION E: FULL CANDIDATE RANKING TABLE */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Screening Rankings & Evaluation Matrix</h3>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
              Select 2 to 5 candidates using checkboxes to compare side-by-side.
            </p>
          </div>

          {/* Search & Filters */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <div style={{ position: 'relative', width: '240px' }}>
              <Search size={15} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '12px' }} />
              <input
                type="text"
                placeholder="Search candidate name / skill..."
                className="input-text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ paddingLeft: '32px', fontSize: '0.8rem' }}
              />
            </div>

            <select
              className="select-control"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              style={{ width: '150px', fontSize: '0.8rem' }}
            >
              <option value="All">All Categories</option>
              <option value="Strong Fit">Strong Fit</option>
              <option value="Potential Fit">Potential Fit</option>
              <option value="Skill Gap">Skill Gap</option>
              <option value="Not Suitable">Not Suitable</option>
            </select>

            <select
              className="select-control"
              value={minExpFilter}
              onChange={(e) => setMinExpFilter(parseFloat(e.target.value))}
              style={{ width: '130px', fontSize: '0.8rem' }}
            >
              <option value={0}>Exp: Any</option>
              <option value={1}>≥ 1 Year</option>
              <option value={2}>≥ 2 Years</option>
              <option value={3}>≥ 3 Years</option>
            </select>

            <button
              className="btn btn-secondary btn-sm"
              onClick={() => {
                const cands = dashboardData?.all_candidates || [];
                if (cands.length >= 2) {
                  const shuffled = [...cands].sort(() => 0.5 - Math.random());
                  setSelectedForCompare(shuffled.slice(0, 2).map(c => c.candidate_id));
                  onOpenComparison();
                }
              }}
              title="Randomly choose 2 resumes to compare"
            >
              <Shuffle size={14} color="#818cf8" />
              <span>Random 2</span>
            </button>

            {(dashboardData?.all_candidates || []).length >= 3 && (
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  const cands = dashboardData?.all_candidates || [];
                  if (cands.length >= 3) {
                    const shuffled = [...cands].sort(() => 0.5 - Math.random());
                    setSelectedForCompare(shuffled.slice(0, 3).map(c => c.candidate_id));
                    onOpenComparison();
                  }
                }}
                title="Randomly choose 3 resumes to compare"
              >
                <Shuffle size={14} color="#34d399" />
                <span>Random 3</span>
              </button>
            )}
          </div>
        </div>

        {/* Table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                <th style={{ padding: '10px 14px', width: '40px' }}>Compare</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Rank</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Candidate</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Category</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Match Score</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Experience</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Critical Skills Match</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8' }}>Claim/Risk Status</th>
                <th style={{ padding: '10px 14px', fontSize: '0.78rem', color: '#94a3b8', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCandidates.map((cand) => {
                const isSelected = selectedForCompare.includes(cand.candidate_id);
                const hasRisks = cand.risks.some(r => r.severity === 'Medium' || r.severity === 'High');
                const hasClaims = cand.claims.some(c => c.status !== 'Verified');

                return (
                  <tr 
                    key={cand.candidate_id} 
                    style={{ 
                      borderBottom: '1px solid rgba(255,255,255,0.04)',
                      background: isSelected ? 'rgba(99, 102, 241, 0.08)' : 'transparent',
                      transition: 'background 0.2s ease'
                    }}
                  >
                    <td style={{ padding: '12px 14px' }}>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleCheckboxToggle(cand.candidate_id)}
                        style={{ accentColor: '#6366f1', cursor: 'pointer' }}
                      />
                    </td>
                    <td style={{ padding: '12px 14px', fontWeight: 800, fontSize: '0.85rem', color: cand.rank <= 3 ? '#34d399' : '#f8fafc' }}>
                      #{cand.rank}
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <span 
                        onClick={() => onSelectCandidate(cand.candidate_id)}
                        style={{ fontWeight: 700, fontSize: '0.85rem', color: '#f8fafc', cursor: 'pointer', textDecoration: 'underline', textDecorationColor: 'rgba(255,255,255,0.2)' }}
                      >
                        {formatCandidateDisplayName(cand)}
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <span className={`badge ${cand.category === 'Strong Fit' ? 'pill-fit-strong' : (cand.category === 'Potential Fit' ? 'pill-fit-potential' : 'pill-fit-gap')}`}>
                        {cand.category}
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontWeight: 800, fontSize: '0.875rem', fontFamily: 'var(--font-mono)', color: '#f8fafc' }}>
                          {cand.overall_score}%
                        </span>
                        {/* Mini bar */}
                        <div style={{ width: '60px', height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '9999px', overflow: 'hidden' }}>
                          <div style={{ width: `${cand.overall_score}%`, height: '100%', background: cand.overall_score >= 85 ? '#10b981' : (cand.overall_score >= 70 ? '#3b82f6' : '#f59e0b') }} />
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px', fontSize: '0.8rem', color: '#cbd5e1' }}>
                      {cand.profile?.total_experience_years || 2.0} yrs
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                        {cand.skill_matches.filter(m => m.importance === 'critical').map(m => (
                          <span key={m.skill} className={`badge ${m.match_level === 'Strong' ? 'badge-strong' : (m.match_level === 'Partial' ? 'badge-partial' : 'badge-missing')}`} style={{ fontSize: '0.65rem' }}>
                            {m.skill}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      {hasRisks || hasClaims ? (
                        <span className="badge badge-weak" style={{ fontSize: '0.68rem' }}>
                          Needs Verification
                        </span>
                      ) : (
                        <span className="badge badge-strong" style={{ fontSize: '0.68rem' }}>
                          Verified
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '12px 14px', textAlign: 'right' }}>
                      <button 
                        className="btn btn-secondary btn-sm"
                        onClick={() => onSelectCandidate(cand.candidate_id)}
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Floating Comparison Action Bar */}
      {selectedForCompare.length >= 2 && (
        <div style={{
          position: 'fixed',
          bottom: '24px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: '#0f172a',
          border: '1px solid #6366f1',
          padding: '12px 24px',
          borderRadius: '9999px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          zIndex: 900
        }}>
          <span style={{ fontSize: '0.85rem', color: '#f8fafc', fontWeight: 600 }}>
            {selectedForCompare.length} candidates selected for matrix
          </span>
          <button className="btn btn-primary btn-sm" onClick={onOpenComparison}>
            <Scale size={15} />
            <span>Compare Now</span>
          </button>
          <button 
            style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '0.75rem' }}
            onClick={() => setSelectedForCompare([])}
          >
            Clear
          </button>
        </div>
      )}
    </div>
  );
}
