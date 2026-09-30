import React, { useState } from 'react';
import { X, UploadCloud, FileText, CheckCircle } from 'lucide-react';

export default function JobUploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [tab, setTab] = useState('paste'); // 'paste' | 'file'
  const [title, setTitle] = useState('Software Engineer');
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      if (tab === 'file' && file) {
        formData.append('file', file);
      } else {
        if (!text.trim()) {
          setError('Please provide the Job Description text.');
          setLoading(false);
          return;
        }
        formData.append('text', text);
      }
      if (title.trim()) {
        formData.append('title', title);
      }

      const res = await fetch('/api/jd/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to parse Job Description');
      }

      const data = await res.json();
      onUploadSuccess(data);
      onClose();
    } catch (err) {
      setError(err.message || 'An error occurred during upload.');
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
              background: 'rgba(99, 102, 241, 0.2)',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <FileText size={20} color="#818cf8" />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Job Description Intelligence Engine</h3>
              <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                Upload or paste JD to extract skills, experience, and critical requirements.
              </p>
            </div>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: '#cbd5e1', display: 'block', marginBottom: '6px' }}>
              Target Job Title
            </label>
            <input 
              type="text" 
              className="input-text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Software Engineer, Backend Engineer"
              required
            />
          </div>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
            <button
              type="button"
              className={`btn btn-sm ${tab === 'paste' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTab('paste')}
            >
              Paste Text
            </button>
            <button
              type="button"
              className={`btn btn-sm ${tab === 'file' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTab('file')}
            >
              Upload Document (PDF / DOCX / TXT)
            </button>
          </div>

          {tab === 'paste' ? (
            <div style={{ marginBottom: '16px' }}>
              <textarea
                className="input-text"
                rows="8"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste the complete Job Description here..."
                style={{ resize: 'vertical' }}
              />
            </div>
          ) : (
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
                id="jdFileInput"
                accept=".pdf,.docx,.txt"
                onChange={(e) => setFile(e.target.files[0])}
                style={{ display: 'none' }}
              />
              <label htmlFor="jdFileInput" style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <UploadCloud size={38} color="#818cf8" style={{ marginBottom: '10px' }} />
                <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#f8fafc' }}>
                  {file ? file.name : "Click to select or drag & drop JD file"}
                </span>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '4px' }}>
                  Supports PDF, DOCX, and TXT files
                </span>
              </label>
            </div>
          )}

          {error && (
            <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#f87171', fontSize: '0.8rem', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Analyzing Semantic Requirements..." : "Analyze & Extract Requirements"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
