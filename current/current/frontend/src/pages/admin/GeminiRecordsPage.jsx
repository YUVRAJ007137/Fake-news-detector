import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaRobot, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { toast } from 'react-toastify';

const GeminiRecordsPage = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGeminiRecords();
  }, []);

  const loadGeminiRecords = async () => {
    try {
      const data = await adminService.getGeminiRecords();
      setRecords(data.records || []);
    } catch (err) {
      toast.error('Failed to load Gemini audit telemetry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="mb-4">
          <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <FaRobot className="text-danger" /> Google Gemini Verification Records
          </h4>
          <p className="text-muted small mb-0">
            Audit log of all LLM claim evaluations, evidence summaries, sources retrieved, and model agreement states.
          </p>
        </div>

        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>Record ID</th>
                <th>Prediction ID</th>
                <th>Gemini Assessment</th>
                <th>Agreement Status</th>
                <th>Evidence Summary Preview</th>
                <th>Entities / Sources</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">Loading Gemini audit telemetry...</td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">No Gemini analysis records stored yet.</td>
                </tr>
              ) : (
                records.map((r) => (
                  <tr key={r.id}>
                    <td>#{r.id}</td>
                    <td>
                      <span className="badge bg-light text-dark border">Pred #{r.prediction_history_id}</span>
                    </td>
                    <td>
                      <span className={`badge ${r.assessment === 'REAL' ? 'bg-success' : r.assessment === 'FAKE' ? 'bg-danger' : 'bg-warning text-dark'}`}>
                        {r.assessment}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${r.agreement_status === 'AGREE' ? 'bg-success' : 'bg-warning text-dark'}`}>
                        {r.agreement_status}
                      </span>
                    </td>
                    <td className="small text-muted text-truncate" style={{ maxWidth: '300px' }}>
                      {r.evidence_summary}
                    </td>
                    <td className="small text-muted">
                      {Array.isArray(r.sources) && r.sources.length > 0 ? r.sources.join(', ') : 'Foundational Knowledge'}
                    </td>
                    <td className="small text-muted">
                      {r.created_at ? new Date(r.created_at).toLocaleString() : '-'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default GeminiRecordsPage;
