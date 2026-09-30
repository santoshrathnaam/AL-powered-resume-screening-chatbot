import React, { useState, useRef, useEffect } from 'react';
import { 
  BotMessageSquare, 
  Send, 
  Sparkles, 
  User, 
  HelpCircle, 
  Scale, 
  FileQuestion, 
  Zap, 
  Filter 
} from 'lucide-react';

export default function AiRecruiterPage({ onSelectCandidate, anonymize }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hello! I am your **TalentLens AI Recruitment Assistant**. 

I have thoroughly parsed and evaluated all candidate profiles against the **Software Engineer** job requirements using explainable NLP and evidence extraction.

You can ask me anything about candidate rankings, skill evidence, or interview preparation. Try one of the suggested prompts below or ask a custom question!`
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedFollowups, setSuggestedFollowups] = useState([
    "Randomly pick 2 candidates to compare",
    "Who is the best candidate to hire?",
    "Why is Candidate #01 ranked first?",
    "Compare Candidate #01 and Candidate #02",
    "Who has the strongest Java experience?",
    "Which candidates are missing AWS?",
    "Draft an interview invitation for Candidate #01",
    "Draft a job offer letter for Candidate #01",
    "Any red flags or timeline gaps in Candidate #09?"
  ]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const newMessages = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          history: newMessages.map(m => ({ role: m.role, content: m.content }))
        })
      });

      if (!res.ok) {
        throw new Error('Chat service encountered an error.');
      }

      const data = await res.json();
      setMessages([...newMessages, { role: 'assistant', content: data.response, relevantCandidates: data.relevant_candidates }]);
      if (data.suggested_followups && data.suggested_followups.length > 0) {
        setSuggestedFollowups(data.suggested_followups);
      }
    } catch (e) {
      setMessages([...newMessages, { 
        role: 'assistant', 
        content: "I apologize, but I encountered an error retrieving grounded candidate context. Please try again." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header */}
      <div className="glass-panel" style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
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
            <BotMessageSquare size={22} color="#ffffff" />
          </div>
          <div>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 800 }}>AI Recruiter Conversational Copilot</h2>
            <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
              Ask grounded questions about rankings, candidate comparisons, claim verifications, and interview readiness.
            </p>
          </div>
        </div>

        <span className="badge badge-strong" style={{ padding: '6px 12px' }}>
          Grounded Context: Active
        </span>
      </div>

      {/* Suggested Quick Prompt Pills */}
      <div>
        <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#94a3b8', display: 'block', marginBottom: '8px' }}>
          Suggested Inquiries:
        </span>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {suggestedFollowups.map((pill, idx) => (
            <button
              key={idx}
              className="btn btn-secondary btn-sm"
              onClick={() => sendMessage(pill)}
              style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.03)' }}
            >
              <Sparkles size={12} color="#818cf8" />
              <span>{pill}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="glass-panel" style={{
        padding: '24px',
        minHeight: '440px',
        maxHeight: '600px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '18px'
      }}>
        {messages.map((m, idx) => {
          const isUser = m.role === 'user';
          return (
            <div 
              key={idx}
              style={{
                display: 'flex',
                gap: '14px',
                alignItems: 'flex-start',
                justifyContent: isUser ? 'flex-end' : 'flex-start'
              }}
            >
              {!isUser && (
                <div style={{
                  background: 'rgba(99, 102, 241, 0.2)',
                  border: '1px solid rgba(99, 102, 241, 0.4)',
                  width: '32px',
                  height: '32px',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  <BotMessageSquare size={17} color="#818cf8" />
                </div>
              )}

              <div style={{
                maxWidth: '82%',
                background: isUser ? 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)' : 'rgba(255, 255, 255, 0.03)',
                border: isUser ? 'none' : '1px solid rgba(255, 255, 255, 0.08)',
                color: '#f8fafc',
                padding: '14px 18px',
                borderRadius: '12px',
                fontSize: '0.85rem',
                lineHeight: '1.6',
                boxShadow: isUser ? '0 4px 12px rgba(99, 102, 241, 0.3)' : 'none'
              }}>
                <div style={{ whiteSpace: 'pre-wrap' }}>
                  {m.content}
                </div>

                {/* Relevant Candidate Quick Link Buttons */}
                {m.relevantCandidates && m.relevantCandidates.length > 0 && (
                  <div style={{ marginTop: '12px', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '8px', display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>View in Intelligence Page:</span>
                    {m.relevantCandidates.map(cid => (
                      <button
                        key={cid}
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '2px 8px', fontSize: '0.7rem' }}
                        onClick={() => onSelectCandidate(cid)}
                      >
                        Inspect {cid}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {isUser && (
                <div style={{
                  background: 'rgba(255, 255, 255, 0.1)',
                  width: '32px',
                  height: '32px',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  <User size={16} color="#cbd5e1" />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center', color: '#94a3b8', fontSize: '0.8rem' }}>
            <div style={{
              background: 'rgba(99, 102, 241, 0.2)',
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <BotMessageSquare size={17} color="#818cf8" />
            </div>
            <span>Analyzing candidate evidence and synthesized metrics...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          className="input-text"
          placeholder="Ask AI Recruiter (e.g. 'Why is Candidate 7 #1?' or 'Compare Candidate 7 and Candidate 14')..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          style={{ padding: '14px 18px', fontSize: '0.9rem' }}
        />
        <button 
          className="btn btn-primary"
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          style={{ padding: '0 24px' }}
        >
          <Send size={18} />
          <span>Send</span>
        </button>
      </div>
    </div>
  );
}
