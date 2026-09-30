import React, { useState } from 'react';
import { X, UploadCloud, FileCheck, CheckCircle2, RotateCcw, AlertTriangle } from 'lucide-react';

export default function ResumeUploadModal({ isOpen, onClose, onUploadSuccess, onResetDemo }) {
  const [files, setFiles] = useState([]);
  const [replacePool, setReplacePool] = useState(true);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!files.length) {
      setError('Please select at least 1 resume file.');
      return;
    }

    setLoading(true);
    setError('');
    setProgress(`Uploading & parsing ${files.length} resume(s)...`);

    try {
      const formData = new FormData();
      for (const f of files) {
        formData.append('files', f);
      }
      formData.append('replace', replacePool ? 'true' : 'false');

      const res = await fetch('/api/resumes/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to parse resumes');
      }

      const data = await res.json();
      setProgress(`Successfully screened ${files.length} resume(s)!`);
      setTimeout(() => {
        onUploadSuccess(data);
        onClose();
      }, 700);
    } catch (err) {
      setError(err.message || 'An error occurred during resume parsing.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '640px', padding: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              background: 'rgba(16, 185, 129, 0.2)',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <UploadCloud size={20} color="#34d399" />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Screen Custom Resumes</h3>
              <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                Upload 1 to 20+ resumes (PDF, DOCX, TXT) to parse, evaluate, and rank.
              </p>
            </div>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        {/* Demo Option Banner */}
        <div style={{
          background: 'rgba(99, 102, 241, 0.08)',
          border: '1px solid rgba(99, 102, 241, 0.2)',
          borderRadius: '10px',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '20px'
        }}>
          <div>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc', display: 'block' }}>
              Want to reload the 20 benchmark resumes instead?
            </span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
              Instant 1-click reload for demo tests and What-If simulations.
            </span>
          </div>
          <button
            type="button"
            className="btn btn-outline-primary btn-sm"
            onClick={() => {
              onResetDemo();
              onClose();
            }}
          >
            <RotateCcw size={14} />
            <span>Load 20 Demo Resumes</span>
          </button>
        </div>

        <form onSubmit={handleUpload}>
          <div style={{
            border: '2px dashed rgba(255,255,255,0.15)',
            borderRadius: '12px',
            padding: '30px 20px',
            textAlign: 'center',
            marginBottom: '16px',
            background: 'rgba(255,255,255,0.01)',
            cursor: 'pointer'
          }}>
            <input
              type="file"
              id="resumeBatchInput"
              multiple
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <label htmlFor="resumeBatchInput" style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <UploadCloud size={38} color="#10b981" style={{ marginBottom: '10px' }} />
              <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#f8fafc' }}>
                {files.length > 0 ? `${files.length} resume file(s) selected` : "Click or drag & drop resume files here"}
              </span>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>
                Supports PDF, DOCX, and TXT files
              </span>
            </label>
          </div>

          {/* Replacement vs Append Toggle */}
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px 14px', borderRadius: '8px', marginBottom: '16px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer', fontSize: '0.825rem', color: '#f8fafc' }}>
              <input
                type="checkbox"
                checked={replacePool}
                onChange={(e) => setReplacePool(e.target.checked)}
                style={{ accentColor: '#10b981', width: '16px', height: '16px', cursor: 'pointer' }}
              />
              <span>
                <strong>Replace current pool with these uploaded resumes</strong> (Recommended)
              </span>
            </label>
            <p style={{ fontSize: '0.72rem', color: '#94a3b8', marginLeft: '26px', marginTop: '2px' }}>
              {replacePool 
                ? "Your uploaded resumes will be ranked starting at Candidate #01." 
                : "Uploaded resumes will be appended to the current list."}
            </p>
          </div>

          {files.length > 0 && (
            <div style={{ maxHeight: '120px', overflowY: 'auto', background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.75rem', color: '#cbd5e1' }}>
              <div style={{ fontWeight: 600, marginBottom: '6px' }}>Selected files ({files.length}):</div>
              {files.map((f, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '2px' }}>
                  <FileCheck size={12} color="#10b981" />
                  <span>{f.name} ({(f.size / 1024).toFixed(1)} KB)</span>
                </div>
              ))}
            </div>
          )}

          {progress && (
            <div style={{ padding: '8px 12px', background: 'rgba(16, 185, 129, 0.15)', borderRadius: '6px', color: '#34d399', fontSize: '0.8rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <CheckCircle2 size={16} />
              <span>{progress}</span>
            </div>
          )}

          {error && (
            <div style={{ padding: '8px 12px', background: 'rgba(239, 68, 68, 0.15)', borderRadius: '6px', color: '#f87171', fontSize: '0.8rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading || !files.length}>
              {loading ? "Screening Uploaded Resumes..." : `Screen ${files.length || ''} Resume(s)`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
