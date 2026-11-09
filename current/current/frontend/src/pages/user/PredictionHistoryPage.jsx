import React, { useState, useEffect } from 'react';
import { newsService } from '../../services/newsService';
import {
  FaHistory, FaSearch, FaCheckCircle, FaExclamationTriangle,
  FaQuestionCircle, FaBookmark, FaEye, FaTimes
} from 'react-icons/fa';
import { toast } from 'react-toastify';

const PredictionHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [labelFilter, setLabelFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, [labelFilter]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await newsService.getHistory(labelFilter, searchQuery);
      setHistory(data.history || []);
    } catch (err) {
      toast.error('Failed to load prediction history.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  const handleSaveArticle = async (newsId) => {
    try {
      await newsService.saveNews(newsId);
      toast.success('News article saved to bookmarks!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to save news.');
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
          <div>
            <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
              <FaHistory className="text-primary" /> Prediction History
            </h4>
            <p className="text-muted small mb-0">
              Browse, filter, and audit your personal fake news prediction records.
            </p>
          </div>

          {/* Search Form */}
          <form onSubmit={handleSearchSubmit} className="d-flex gap-2">
            <input
              type="text"
              className="form-control form-control-sm"
              placeholder="Search by keywords..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="btn btn-primary btn-sm d-flex align-items-center gap-1">
              <FaSearch /> Search
            </button>
          </form>
        </div>

        {/* Filter Buttons */}
        <div className="d-flex flex-wrap gap-2 mb-4">
          <button
            onClick={() => setLabelFilter('')}
            className={`btn btn-sm ${labelFilter === '' ? 'btn-primary' : 'btn-outline-secondary'}`}
          >
            All Predictions
          </button>
          <button
            onClick={() => setLabelFilter('REAL')}
            className={`btn btn-sm ${labelFilter === 'REAL' ? 'btn-success' : 'btn-outline-success'}`}
          >
            Verified Real
          </button>
          <button
            onClick={() => setLabelFilter('FAKE')}
            className={`btn btn-sm ${labelFilter === 'FAKE' ? 'btn-danger' : 'btn-outline-danger'}`}
          >
            Flagged Fake
          </button>
          <button
            onClick={() => setLabelFilter('INCONCLUSIVE')}
            className={`btn btn-sm ${labelFilter === 'INCONCLUSIVE' ? 'btn-warning' : 'btn-outline-warning'}`}
          >
            Inconclusive
          </button>
        </div>

        {/* History Table */}
        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>Title / Headline</th>
                <th>Category</th>
                <th>Verdict</th>
                <th>Confidence</th>
                <th>Engine</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">Loading history records...</td>
                </tr>
              ) : history.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">
                    No prediction records matched your filter criteria.
                  </td>
                </tr>
              ) : (
                history.map((item) => {
                  const isR = item.prediction_label === 'REAL';
                  const isF = item.prediction_label === 'FAKE';
                  return (
                    <tr key={item.id}>
                      <td className="fw-semibold text-truncate" style={{ maxWidth: '280px' }}>
                        {item.news_title}
                      </td>
                      <td>
                        <span className="badge bg-light text-dark border">{item.category}</span>
                      </td>
                      <td>
                        <span className={isR ? 'badge-real' : isF ? 'badge-fake' : 'badge-inconclusive'}>
                          {item.prediction_label}
                        </span>
                      </td>
                      <td className="fw-semibold">
                        {(item.confidence_score * 100).toFixed(1)}%
                      </td>
                      <td className="small text-muted">{item.analysis_type}</td>
                      <td className="small text-muted">
                        {item.created_at ? new Date(item.created_at).toLocaleDateString() : '-'}
                      </td>
                      <td>
                        <div className="d-flex gap-1">
                          <button
                            onClick={() => setSelectedItem(item)}
                            className="btn btn-outline-primary btn-sm px-2 py-1"
                            title="Inspect Record Details"
                          >
                            <FaEye />
                          </button>
                          <button
                            onClick={() => handleSaveArticle(item.news_id)}
                            className="btn btn-outline-secondary btn-sm px-2 py-1"
                            title="Bookmark News"
                          >
                            <FaBookmark />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal / Detail View */}
      {selectedItem && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content shadow">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">Prediction Record #{selectedItem.id}</h5>
                <button type="button" className="btn-close" onClick={() => setSelectedItem(null)}></button>
              </div>
              <div className="modal-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <span className={selectedItem.prediction_label === 'REAL' ? 'badge-real' : selectedItem.prediction_label === 'FAKE' ? 'badge-fake' : 'badge-inconclusive'}>
                    {selectedItem.prediction_label}
                  </span>
                  <span className="text-muted small">
                    Confidence: <strong>{(selectedItem.confidence_score * 100).toFixed(1)}%</strong>
                  </span>
                </div>

                <h5 className="fw-bold text-dark">{selectedItem.news_title}</h5>
                <p className="small text-muted mb-3">
                  <strong>Category:</strong> {selectedItem.category} &bull; <strong>Source:</strong> {selectedItem.source} &bull; <strong>Model:</strong> {selectedItem.model_version}
                </p>

                <div className="p-3 bg-light rounded border mb-3" style={{ maxHeight: '200px', overflowY: 'auto' }}>
                  <small className="text-dark">{selectedItem.news_article}</small>
                </div>

                {selectedItem.gemini_verification && (
                  <div className="alert alert-light border p-3">
                    <strong className="text-primary d-block mb-1">Gemini Verification:</strong>
                    <p className="small mb-1">{selectedItem.gemini_verification.evidence_summary}</p>
                    <span className="badge bg-secondary">
                      Consensus: {selectedItem.gemini_verification.agreement_status}
                    </span>
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => setSelectedItem(null)}
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

export default PredictionHistoryPage;
