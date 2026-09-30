import React, { useEffect, useState } from 'react';
import { X, Scale, Award, Check, AlertCircle, Shuffle } from 'lucide-react';

export default function ComparisonModal({ isOpen, onClose, candidateIds, allCandidates = [], onSelectCandidates, anonymize }) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    if (isOpen && candidateIds && candidateIds.length >= 2) {
      fetchComparison();
    }
  }, [isOpen, candidateIds]);

  const fetchComparison = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ candidate_ids: candidateIds })
      });
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (e) {
      console.error("Comparison fetch failed:", e);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '960px', padding: '28px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              background: 'rgba(16, 185, 129, 0.2)',
              border: '1px solid rgba(16, 185, 129, 0.4)',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Scale size={20} color="#34d399" />
            </div>
            <div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Side-by-Side Candidate Comparison</h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                Comparing technical credentials, experience depth, and trade-offs.
              </p>
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {allCandidates && allCandidates.length >= 2 && (
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  const shuffled = [...allCandidates].sort(() => 0.5 - Math.random());
                  const pair = shuffled.slice(0, 2).map(c => c.candidate_id);
                  if (onSelectCandidates) onSelectCandidates(pair);
                }}
                title="Randomly choose 2 resumes to compare"
              >
                <Shuffle size={13} color="#818cf8" />
                <span>Random 2</span>
              </button>
            )}

            {allCandidates && allCandidates.length >= 3 && (
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  const shuffled = [...allCandidates].sort(() => 0.5 - Math.random());
                  const trio = shuffled.slice(0, 3).map(c => c.candidate_id);
                  if (onSelectCandidates) onSelectCandidates(trio);
                }}
                title="Randomly choose 3 resumes to compare"
              >
                <Shuffle size={13} color="#34d399" />
                <span>Random 3</span>
              </button>
            )}

            <button 
              onClick={onClose}
              style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>
            Evaluating candidates across multi-dimensional criteria...
          </div>
        ) : data ? (
          <div>
            {/* Comparison Table */}
            <div style={{ overflowX: 'auto', marginBottom: '20px' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                  <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                    <th style={{ padding: '12px 16px', fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>Criteria</th>
                    {data.candidates.map(c => (
                      <th key={c.candidate_id} style={{ padding: '12px 16px', fontSize: '0.85rem', color: '#f8fafc', fontWeight: 700 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span>{anonymize ? c.anonymized_id : c.candidate_id}</span>
                          <span className="badge badge-strong" style={{ fontSize: '0.7rem', padding: '2px 6px' }}>
                            #{c.rank} ({c.overall_score}%)
                          </span>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.matrix.map((row, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)', background: idx % 2 === 0 ? 'rgba(255,255,255,0.01)' : 'transparent' }}>
                      <td style={{ padding: '12px 16px', fontWeight: 600, fontSize: '0.825rem', color: '#cbd5e1' }}>
                        {row.criteria}
                        {row.notes && <span style={{ display: 'block', fontSize: '0.7rem', color: '#64748b', fontWeight: 400 }}>{row.notes}</span>}
                      </td>
                      {data.candidates.map(c => {
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
                                <Award size={14} color="#10b981" title="Top performance in this dimension" />
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

            {/* Differentiators Summary Card */}
            <div style={{ background: 'rgba(99, 102, 241, 0.06)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <AlertCircle size={16} color="#818cf8" />
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc' }}>
                  AI Comparative Differentiators & Analysis
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: '#cbd5e1', marginBottom: '10px' }}>
                {data.summary}
              </p>
              <ul style={{ paddingLeft: '20px', fontSize: '0.8rem', color: '#94a3b8' }}>
                {data.key_differentiators.map((d, i) => (
                  <li key={i} style={{ marginBottom: '4px' }}>{d}</li>
                ))}
              </ul>
            </div>
          </div>
        ) : null}

        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
          <button className="btn btn-secondary" onClick={onClose}>
            Close Matrix
          </button>
        </div>
      </div>
    </div>
  );
}
