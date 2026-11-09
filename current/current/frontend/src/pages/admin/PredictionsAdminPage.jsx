import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaHistory, FaEye, FaSearch } from 'react-icons/fa';
import { toast } from 'react-toastify';

const PredictionsAdminPage = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [labelFilter, setLabelFilter] = useState('');
  const [selectedRecord, setSelectedRecord] = useState(null);

  useEffect(() => {
    fetchPredictions();
  }, [labelFilter]);

  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const data = await adminService.getPredictions(labelFilter);
      setPredictions(data.predictions || []);
    } catch (err) {
      toast.error('Failed to load prediction telemetry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
          <div>
            <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
              <FaHistory className="text-danger" /> System-Wide Detected News Records
            </h4>
            <p className="text-muted small mb-0">
              Audit log of all classification events generated across User inputs and batch File uploads.
            </p>
          </div>

          <div className="d-flex gap-2">
            <button
              onClick={() => setLabelFilter('')}
              className={`btn btn-sm ${labelFilter === '' ? 'btn-primary' : 'btn-outline-secondary'}`}
            >
              All Records
            </button>
            <button
              onClick={() => setLabelFilter('REAL')}
              className={`btn btn-sm ${labelFilter === 'REAL' ? 'btn-success' : 'btn-outline-success'}`}
            >
              Real
            </button>
            <button
              onClick={() => setLabelFilter('FAKE')}
              className={`btn btn-sm ${labelFilter === 'FAKE' ? 'btn-danger' : 'btn-outline-danger'}`}
            >
              Fake
            </button>
            <button
              onClick={() => setLabelFilter('INCONCLUSIVE')}
              className={`btn btn-sm ${labelFilter === 'INCONCLUSIVE' ? 'btn-warning' : 'btn-outline-warning'}`}
            >
              Inconclusive
            </button>
          </div>
        </div>

        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>News Title</th>
                <th>Category</th>
                <th>Label</th>
                <th>Confidence</th>
                <th>Engine</th>
                <th>User ID</th>
                <th>Timestamp</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="9" className="text-center py-4 text-muted">Loading records...</td>
                </tr>
              ) : predictions.length === 0 ? (
                <tr>
                  <td colSpan="9" className="text-center py-4 text-muted">No prediction records found.</td>
                </tr>
              ) : (
                predictions.map((p) => {
                  const isR = p.prediction_label === 'REAL';
                  const isF = p.prediction_label === 'FAKE';
                  return (
                    <tr key={p.id}>
                      <td>#{p.id}</td>
                      <td className="fw-semibold text-truncate" style={{ maxWidth: '240px' }}>
                        {p.news_title}
                      </td>
                      <td>
                        <span className="badge bg-light text-dark border">{p.category}</span>
                      </td>
                      <td>
                        <span className={isR ? 'badge-real' : isF ? 'badge-fake' : 'badge-inconclusive'}>
                          {p.prediction_label}
                        </span>
                      </td>
                      <td className="fw-semibold">{(p.confidence_score * 100).toFixed(1)}%</td>
                      <td className="small text-muted">{p.analysis_type}</td>
                      <td>{p.user_id ? `#${p.user_id}` : 'Anonymous'}</td>
                      <td className="small text-muted">
                        {p.created_at ? new Date(p.created_at).toLocaleString() : '-'}
                      </td>
                      <td>
                        <button
                          onClick={() => setSelectedRecord(p)}
                          className="btn btn-outline-primary btn-sm px-2 py-1"
                          title="View Full Content"
                        >
                          <FaEye />
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Inspect Modal */}
      {selectedRecord && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content shadow">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">Prediction Record #{selectedRecord.id}</h5>
                <button type="button" className="btn-close" onClick={() => setSelectedRecord(null)}></button>
              </div>
              <div className="modal-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <span className={selectedRecord.prediction_label === 'REAL' ? 'badge-real' : selectedRecord.prediction_label === 'FAKE' ? 'badge-fake' : 'badge-inconclusive'}>
                    {selectedRecord.prediction_label}
                  </span>
                  <span>Confidence: <strong>{(selectedRecord.confidence_score * 100).toFixed(1)}%</strong></span>
                </div>

                <h5 className="fw-bold">{selectedRecord.news_title}</h5>
                <div className="p-3 bg-light rounded border mb-3" style={{ maxHeight: '250px', overflowY: 'auto' }}>
                  <small>{selectedRecord.news_article}</small>
                </div>

                {selectedRecord.gemini_verification && (
                  <div className="alert alert-light border p-3">
                    <strong className="text-primary d-block mb-1">Gemini Verification:</strong>
                    <p className="small mb-1">{selectedRecord.gemini_verification.evidence_summary}</p>
                    <span className="badge bg-secondary">
                      Consensus: {selectedRecord.gemini_verification.agreement_status}
                    </span>
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => setSelectedRecord(null)}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionsAdminPage;
