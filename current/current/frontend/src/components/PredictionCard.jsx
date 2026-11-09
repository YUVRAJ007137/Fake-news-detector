import React, { useState } from 'react';
import {
  FaCheckCircle, FaExclamationTriangle, FaQuestionCircle,
  FaBookmark, FaRobot, FaExternalLinkAlt, FaClock
} from 'react-icons/fa';
import { newsService } from '../services/newsService';
import { toast } from 'react-toastify';

const PredictionCard = ({ result, newsId, onSaveSuccess }) => {
  const [saving, setSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  if (!result) return null;

  const label = (result.overall_decision || result.prediction_label || 'INCONCLUSIVE').toUpperCase();
  const confidence = result.confidence_score !== undefined && result.confidence_score !== null
    ? (result.confidence_score * 100).toFixed(1)
    : '50.0';

  const isReal = label === 'REAL';
  const isFake = label === 'FAKE';

  const badgeClass = isReal ? 'badge-real' : isFake ? 'badge-fake' : 'badge-inconclusive';
  const fillClass = isReal ? 'fill-real' : isFake ? 'fill-fake' : 'fill-inconclusive';

  const handleSave = async () => {
    const targetNewsId = newsId || result.news_id;
    if (!targetNewsId) {
      toast.warning('This article cannot be bookmarked without an associated news record.');
      return;
    }
    setSaving(true);
    try {
      await newsService.saveNews(targetNewsId);
      setIsSaved(true);
      toast.success('News article saved to your bookmarks!');
      if (onSaveSuccess) onSaveSuccess();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to bookmark news.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card app-card border-0 shadow-sm mt-4">
      <div className="card-header bg-white border-bottom py-3 d-flex flex-wrap justify-content-between align-items-center gap-2">
        <div className="d-flex align-items-center gap-2">
          <span className={badgeClass}>
            {isReal && <FaCheckCircle />}
            {isFake && <FaExclamationTriangle />}
            {!isReal && !isFake && <FaQuestionCircle />}
            {label}
          </span>
          <span className="text-muted small">
            Confidence: <strong className="text-dark">{confidence}%</strong>
          </span>
          {result.is_cached && (
            <span className="badge bg-light text-secondary border">Cached Prediction</span>
          )}
        </div>

        <div className="d-flex align-items-center gap-2">
          <button
            onClick={handleSave}
            disabled={saving || isSaved}
            className={`btn btn-sm ${isSaved ? 'btn-success' : 'btn-outline-primary'} d-flex align-items-center gap-1`}
          >
            <FaBookmark /> {isSaved ? 'Saved' : saving ? 'Saving...' : 'Save News'}
          </button>
        </div>
      </div>

      <div className="card-body p-4">
        {/* Confidence Progress Bar */}
        <div className="mb-4">
          <div className="d-flex justify-content-between small text-muted mb-1">
            <span>Model Discriminant Confidence</span>
            <span>{confidence}%</span>
          </div>
          <div className="confidence-meter">
            <div
              className={`confidence-fill ${fillClass}`}
              style={{ width: `${confidence}%` }}
            ></div>
          </div>
        </div>

        {/* Gemini verification breakdown if present */}
        {result.gemini_analysis && (
          <div className="alert alert-light border p-3 mb-4 rounded-3">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="fw-semibold text-primary d-flex align-items-center gap-1">
                <FaRobot /> Gemini LLM Claim Verification
              </span>
              <span className={`badge ${result.gemini_analysis.agreement_status === 'AGREE' ? 'bg-success' : 'bg-warning text-dark'}`}>
                Consensus: {result.gemini_analysis.agreement_status}
              </span>
            </div>
            <p className="small mb-2 text-dark">
              {result.gemini_analysis.evidence_summary}
            </p>
            {result.gemini_analysis.sources && result.gemini_analysis.sources.length > 0 && (
              <div className="small text-muted">
                <strong>Referenced Sources:</strong> {result.gemini_analysis.sources.join(', ')}
              </div>
            )}
          </div>
        )}

        {/* Signals and Explanation */}
        <div className="mb-3">
          <h6 className="fw-semibold text-dark mb-1">Linguistic &amp; Model Explanation:</h6>
          <p className="text-muted small mb-3">
            {result.explanation || result.gemini_analysis?.evidence_summary || 'Analysis evaluated against trained linguistic patterns.'}
          </p>

          {result.signals && result.signals.length > 0 && (
            <div>
              <span className="small text-muted d-block mb-1">Key Salient Signal Terms:</span>
              <div className="d-flex flex-wrap gap-1">
                {result.signals.map((sig, idx) => (
                  <span key={idx} className="signal-tag">
                    #{sig}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Metadata Footer */}
        <div className="d-flex flex-wrap justify-content-between align-items-center border-top pt-3 text-muted small mt-4">
          <div>
            <span>Model: <strong>{result.model_version || 'Calibrated-LinearSVC-v1.0.0'}</strong></span>
          </div>
          <div>
            <span>Analysis Mode: <strong>{result.gemini_analysis ? 'Dual-Engine (ML + Gemini)' : 'Local ML Pipeline'}</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionCard;
