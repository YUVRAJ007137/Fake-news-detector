import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { newsService } from '../../services/newsService';
import { fileService } from '../../services/fileService';
import {
  FaTachometerAlt, FaCheckCircle, FaExclamationTriangle,
  FaFileUpload, FaHistory, FaNewspaper, FaRobot, FaArrowRight
} from 'react-icons/fa';

const UserDashboard = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [fileCount, setFileCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const historyData = await newsService.getHistory();
      setHistory(historyData.history || []);

      const fileData = await fileService.getUploadHistory();
      setFileCount(fileData.total || 0);
    } catch (err) {
      console.error('Failed to load user dashboard telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  const totalPredictions = history.length;
  const realCount = history.filter((h) => h.prediction_label === 'REAL').length;
  const fakeCount = history.filter((h) => h.prediction_label === 'FAKE').length;
  const inconclusiveCount = totalPredictions - (realCount + fakeCount);

  return (
    <div>
      {/* Welcome Banner */}
      <div className="card app-card border-0 p-4 mb-4 bg-white shadow-sm">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3">
          <div>
            <h3 className="fw-bold mb-1">Welcome back, {user?.full_name}!</h3>
            <p className="text-muted small mb-0">
             
            </p>
          </div>
          <div className="d-flex gap-2">
            <Link to="/user/previous-news" className="btn btn-primary btn-sm d-flex align-items-center gap-2">
              <FaNewspaper /> Previous News ML
            </Link>
            <Link to="/user/latest-news" className="btn btn-outline-primary btn-sm d-flex align-items-center gap-2">
              <FaRobot /> Latest News &amp; 
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="row g-3 mb-4">
        <div className="col-sm-6 col-xl-3">
          <div className="card app-card border-0 p-3 shadow-sm bg-white h-100">
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <span className="text-muted small fw-semibold d-block">TOTAL ANALYZED</span>
                <h3 className="fw-bold my-1">{loading ? '...' : totalPredictions}</h3>
                <span className="text-muted extra-small">Lifetime predictions</span>
              </div>
              <div className="p-3 bg-primary bg-opacity-10 text-primary rounded-circle">
                <FaTachometerAlt className="fs-4" />
              </div>
            </div>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card border-0 p-3 shadow-sm bg-white h-100">
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <span className="text-muted small fw-semibold d-block">VERIFIED REAL</span>
                <h3 className="fw-bold my-1 text-success">{loading ? '...' : realCount}</h3>
                <span className="text-muted extra-small">Authentic news detected</span>
              </div>
              <div className="p-3 bg-success bg-opacity-10 text-success rounded-circle">
                <FaCheckCircle className="fs-4" />
              </div>
            </div>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card border-0 p-3 shadow-sm bg-white h-100">
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <span className="text-muted small fw-semibold d-block">FLAGGED FAKE</span>
                <h3 className="fw-bold my-1 text-danger">{loading ? '...' : fakeCount}</h3>
                <span className="text-muted extra-small">Disinformation identified</span>
              </div>
              <div className="p-3 bg-danger bg-opacity-10 text-danger rounded-circle">
                <FaExclamationTriangle className="fs-4" />
              </div>
            </div>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card border-0 p-3 shadow-sm bg-white h-100">
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <span className="text-muted small fw-semibold d-block">UPLOADED FILES</span>
                <h3 className="fw-bold my-1 text-info">{loading ? '...' : fileCount}</h3>
                <span className="text-muted extra-small">PDF, DOCX, TXT, CSV</span>
              </div>
              <div className="p-3 bg-info bg-opacity-10 text-info rounded-circle">
                <FaFileUpload className="fs-4" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Launch Cards */}
      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <div className="card app-card p-4 border-0 shadow-sm h-100">
            <h5 className="fw-bold text-primary mb-2">Previous News ML</h5>
            <p className="text-muted small mb-3">
              
            </p>
            <Link to="/user/previous-news" className="mt-auto btn btn-outline-primary btn-sm d-flex align-items-center justify-content-center gap-2">
              Launch Detection <FaArrowRight />
            </Link>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card app-card p-4 border-0 shadow-sm h-100">
            <h5 className="fw-bold text-primary mb-2">Latest News &amp;</h5>
            <p className="text-muted small mb-3">
              
            </p>
            <Link to="/user/latest-news" className="mt-auto btn btn-outline-primary btn-sm d-flex align-items-center justify-content-center gap-2">
              Launch Verification <FaArrowRight />
            </Link>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card app-card p-4 border-0 shadow-sm h-100">
            <h5 className="fw-bold text-primary mb-2">File Upload Ingestion</h5>
            <p className="text-muted small mb-3">
              
            </p>
            <Link to="/user/file-upload" className="mt-auto btn btn-outline-primary btn-sm d-flex align-items-center justify-content-center gap-2">
              Upload Files <FaArrowRight />
            </Link>
          </div>
        </div>
      </div>

      {/* Recent History Table */}
      <div className="card app-card border-0 shadow-sm">
        <div className="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
          <h5 className="fw-bold mb-0 d-flex align-items-center gap-2">
            <FaHistory className="text-primary" /> Recent Prediction History
          </h5>
          <Link to="/user/history" className="btn btn-outline-secondary btn-sm">
            View All ({totalPredictions})
          </Link>
        </div>

        <div className="table-responsive">
          <table className="table table-custom table-hover mb-0">
            <thead>
              <tr>
                <th>Title / Headline</th>
                <th>Category</th>
                <th>Verdict</th>
                <th>Confidence</th>
                <th>Engine</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">Loading telemetry data...</td>
                </tr>
              ) : history.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">
                    No news articles analyzed yet. Try submitting an article above!
                  </td>
                </tr>
              ) : (
                history.slice(0, 6).map((item) => {
                  const isR = item.prediction_label === 'REAL';
                  const isF = item.prediction_label === 'FAKE';
                  return (
                    <tr key={item.id}>
                      <td className="fw-semibold text-truncate" style={{ maxWidth: '320px' }}>
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
                      <td className="small text-muted">
                        {item.analysis_type}
                      </td>
                      <td className="small text-muted">
                        {item.created_at ? new Date(item.created_at).toLocaleDateString() : '-'}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
