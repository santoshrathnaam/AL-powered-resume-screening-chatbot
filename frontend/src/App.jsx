import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';

import Navbar from './components/Navbar';
import DisclaimerBanner from './components/DisclaimerBanner';
import WhatIfModal from './components/WhatIfModal';
import ComparisonModal from './components/ComparisonModal';
import JobUploadModal from './components/JobUploadModal';
import ResumeUploadModal from './components/ResumeUploadModal';

import DashboardPage from './pages/DashboardPage';
import CandidateDetailPage from './pages/CandidateDetailPage';
import AiRecruiterPage from './pages/AiRecruiterPage';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard'); // 'dashboard' | 'candidate' | 'chat'
  const [selectedCandidateId, setSelectedCandidateId] = useState('Candidate #07');
  const [dashboardData, setDashboardData] = useState(null);
  const [anonymize, setAnonymize] = useState(false); // default to false so user immediately sees real candidate names
  const [selectedForCompare, setSelectedForCompare] = useState([]);

  // Modals
  const [whatIfOpen, setWhatIfOpen] = useState(false);
  const [compareOpen, setCompareOpen] = useState(false);
  const [jobUploadOpen, setJobUploadOpen] = useState(false);
  const [resumeUploadOpen, setResumeUploadOpen] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await fetch('/api/dashboard');
      if (res.ok) {
        const json = await res.json();
        setDashboardData(json);
        if (json.top_10 && json.top_10.length > 0) {
          setSelectedCandidateId(json.top_10[0].candidate_id);
          setSelectedForCompare(json.top_10.slice(0, 2).map(c => c.candidate_id));
        }
      }
    } catch (e) {
      console.error("Dashboard fetch error:", e);
    }
  };

  const handleSelectCandidate = (cid) => {
    setSelectedCandidateId(cid);
    setActivePage('candidate');
  };

  const handleUploadResumesSuccess = (data) => {
    setDashboardData(data);
    if (data.top_10 && data.top_10.length > 0) {
      setSelectedCandidateId(data.top_10[0].candidate_id);
      setSelectedForCompare(data.top_10.slice(0, 2).map(c => c.candidate_id));
    }
    // Celebrate successful screening
    try {
      confetti({
        particleCount: 50,
        spread: 70,
        origin: { y: 0.7 },
        colors: ['#10b981', '#6366f1', '#3b82f6']
      });
    } catch (_) {}
  };

  const handleApplyWhatIf = async (weights, importances) => {
    try {
      const res = await fetch('/api/what-if', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          weights,
          requirement_importances: importances
        })
      });
      if (res.ok) {
        const json = await res.json();
        setDashboardData(json);
        try {
          confetti({
            particleCount: 45,
            spread: 60,
            origin: { y: 0.8 },
            colors: ['#6366f1', '#10b981', '#f59e0b']
          });
        } catch (_) {}
      }
    } catch (e) {
      console.error("What-If simulation failed:", e);
    }
  };

  const handleResetDemo = async () => {
    try {
      const res = await fetch('/api/reset-demo', { method: 'POST' });
      if (res.ok) {
        const json = await res.json();
        setDashboardData(json);
        setSelectedCandidateId('Candidate #07');
        setSelectedForCompare(['Candidate #07', 'Candidate #14']);
      }
    } catch (e) {
      console.error("Reset demo failed:", e);
    }
  };

  return (
    <div className="app-container">
      {/* Top HR Disclaimer */}
      <DisclaimerBanner />

      {/* Navigation */}
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        onOpenWhatIf={() => setWhatIfOpen(true)}
        onResetDemo={handleResetDemo}
        anonymize={anonymize}
        setAnonymize={setAnonymize}
        version={dashboardData?.version || 1}
      />

      {/* Main Content Body */}
      <main className="main-content">
        {activePage === 'dashboard' && (
          <DashboardPage
            dashboardData={dashboardData}
            onSelectCandidate={handleSelectCandidate}
            onOpenWhatIf={() => setWhatIfOpen(true)}
            onOpenJobUpload={() => setJobUploadOpen(true)}
            onOpenResumeUpload={() => setResumeUploadOpen(true)}
            onOpenComparison={() => setCompareOpen(true)}
            selectedForCompare={selectedForCompare}
            setSelectedForCompare={setSelectedForCompare}
            anonymize={anonymize}
          />
        )}

        {activePage === 'candidate' && (
          <CandidateDetailPage
            candidateId={selectedCandidateId}
            allCandidates={dashboardData?.all_candidates || []}
            onSelectCandidate={setSelectedCandidateId}
            anonymize={anonymize}
          />
        )}

        {activePage === 'chat' && (
          <AiRecruiterPage
            onSelectCandidate={handleSelectCandidate}
            anonymize={anonymize}
          />
        )}
      </main>

      {/* Modals */}
      <WhatIfModal
        isOpen={whatIfOpen}
        onClose={() => setWhatIfOpen(false)}
        currentWeights={dashboardData?.weights}
        currentImportances={dashboardData?.job?.requirements?.reduce((acc, r) => ({ ...acc, [r.skill]: r.importance }), {})}
        onApply={handleApplyWhatIf}
      />

      <ComparisonModal
        isOpen={compareOpen}
        onClose={() => setCompareOpen(false)}
        candidateIds={selectedForCompare}
        allCandidates={dashboardData?.all_candidates || []}
        onSelectCandidates={(ids) => setSelectedForCompare(ids)}
        anonymize={anonymize}
      />

      <JobUploadModal
        isOpen={jobUploadOpen}
        onClose={() => setJobUploadOpen(false)}
        onUploadSuccess={(data) => setDashboardData(data)}
      />

      <ResumeUploadModal
        isOpen={resumeUploadOpen}
        onClose={() => setResumeUploadOpen(false)}
        onUploadSuccess={handleUploadResumesSuccess}
        onResetDemo={handleResetDemo}
      />

      {/* Enterprise Footer */}
      <footer style={{
        marginTop: '60px',
        borderTop: '1px solid rgba(255, 255, 255, 0.08)',
        background: 'rgba(11, 15, 25, 0.9)',
        padding: '24px 28px',
        fontSize: '0.78rem',
        color: '#64748b',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        <div>
          <strong style={{ color: '#94a3b8' }}>TalentLens AI</strong> — Explainable AI Recruitment Assistant
          <span style={{ margin: '0 8px' }}>•</span>
          Evidence-Based Resume Screening, Candidate Ranking & Interview Intelligence
        </div>
        <div>
          Major Project Demonstration • Built with FastAPI & React
        </div>
      </footer>
    </div>
  );
}
