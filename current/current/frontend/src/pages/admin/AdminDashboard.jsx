import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import {
  FaUsers, FaHistory, FaCheckCircle, FaExclamationTriangle,
  FaDatabase, FaCogs, FaFileUpload, FaRobot
} from 'react-icons/fa';
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, BarElement
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { toast } from 'react-toastify';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const AdminDashboard = () => {
  const [kpis, setKpis] = useState(null);
  const [recentPredictions, setRecentPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await adminService.getDashboardKPIs();
      setKpis(data.kpis);
      setRecentPredictions(data.recent_predictions || []);
    } catch (err) {
      toast.error('Failed to load administrative telemetry.');
    } finally {
      setLoading(false);
    }
  };

  const doughnutData = {
    labels: ['Verified Real', 'Flagged Fake', 'Inconclusive'],
    datasets: [
      {
        data: [
          kpis?.real_predictions || 0,
          kpis?.fake_predictions || 0,
          kpis?.inconclusive_predictions || 0
        ],
        backgroundColor: ['#10b981', '#ef4444', '#f59e0b'],
        borderWidth: 1
      }
    ]
  };

  return (
    <div>
      <div className="card app-card border-0 p-4 mb-4 bg-white shadow-sm">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <h3 className="fw-bold mb-1 text-danger">Administrator Intelligence Console</h3>
            <p className="text-muted small mb-0">
              Global system monitoring, database telemetry, model versioning, and user governance.
            </p>
          </div>
          <span className="badge bg-danger p-2 fs-6">System Status: OPERATIONAL</span>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="row g-3 mb-4">
        <div className="col-sm-6 col-xl-3">
          <div className="card app-card p-3 border-0 shadow-sm bg-white h-100">
            <span className="text-muted small fw-semibold">REGISTERED USERS</span>
            <h3 className="fw-bold my-1 text-primary">{loading ? '...' : kpis?.total_users}</h3>
            <span className="text-muted extra-small">Active citizen users</span>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card p-3 border-0 shadow-sm bg-white h-100">
            <span className="text-muted small fw-semibold">TOTAL PREDICTIONS</span>
            <h3 className="fw-bold my-1 text-dark">{loading ? '...' : kpis?.total_predictions}</h3>
            <span className="text-muted extra-small">Across ML &amp; Gemini</span>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card p-3 border-0 shadow-sm bg-white h-100">
            <span className="text-muted small fw-semibold">ACTIVE MODEL ACCURACY</span>
            <h3 className="fw-bold my-1 text-success">
              {loading ? '...' : `${(kpis?.active_accuracy * 100).toFixed(1)}%`}
            </h3>
            <span className="text-muted extra-small text-truncate d-block">{kpis?.active_model_name}</span>
          </div>
        </div>

        <div className="col-sm-6 col-xl-3">
          <div className="card app-card p-3 border-0 shadow-sm bg-white h-100">
            <span className="text-muted small fw-semibold">REGISTERED DATASETS</span>
            <h3 className="fw-bold my-1 text-info">{loading ? '...' : kpis?.total_datasets}</h3>
            <span className="text-muted extra-small">Self-Generated &bull; Kaggle &bull; Hybrid</span>
          </div>
        </div>
      </div>

      {/* Analytics Charts & Telemetry */}
      <div className="row g-4 mb-4">
        {/* Doughnut Chart */}
        <div className="col-md-5">
          <div className="card app-card p-4 border-0 shadow-sm h-100 bg-white">
            <h5 className="fw-bold mb-3">Prediction Distribution</h5>
            <div style={{ maxHeight: '260px' }} className="d-flex justify-content-center">
              {loading ? (
                <div className="text-muted my-auto">Loading chart metrics...</div>
              ) : (
                <Doughnut data={doughnutData} options={{ maintainAspectRatio: false }} />
              )}
            </div>
          </div>
        </div>

        {/* Global Summary Info */}
        <div className="col-md-7">
          <div className="card app-card p-4 border-0 shadow-sm h-100 bg-white">
            <h5 className="fw-bold mb-3">System Health &amp; Pipeline Architecture</h5>
            <ul className="list-group list-group-flush small">
              <li className="list-group-item d-flex justify-content-between align-items-center px-0 py-2">
                <span>Relational Database Engine</span>
                <span className="badge bg-success">MySQL 8.0+ Compatible / Connected</span>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center px-0 py-2">
                <span>Active Champion Algorithm</span>
                <strong>Calibrated Linear SVM (Platt Scaling)</strong>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center px-0 py-2">
                <span>Feature Extraction Method</span>
                <strong>TF-IDF Vectorizer (Unigram + Bigram, 5,000 Features)</strong>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center px-0 py-2">
                <span>Gemini API Integration</span>
                <span className="badge bg-primary">Google GenAI Official SDK</span>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center px-0 py-2">
                <span>Batch File Parsers</span>
                <span>PDF (pypdf), Word (python-docx), TXT, CSV</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Global Recent Predictions Audit */}
      <div className="card app-card border-0 shadow-sm bg-white">
        <div className="card-header bg-white border-bottom py-3">
          <h5 className="fw-bold mb-0">Global Telemetry: Latest System Predictions</h5>
        </div>
        <div className="table-responsive">
          <table className="table table-custom table-hover mb-0">
            <thead>
              <tr>
                <th>#</th>
                <th>News Title</th>
                <th>Category</th>
                <th>Prediction</th>
                <th>Confidence</th>
                <th>Engine</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {recentPredictions.map((pred) => (
                <tr key={pred.id}>
                  <td>{pred.id}</td>
                  <td className="fw-semibold text-truncate" style={{ maxWidth: '280px' }}>
                    {pred.news_title}
                  </td>
                  <td>
                    <span className="badge bg-light text-dark border">{pred.category}</span>
                  </td>
                  <td>
                    <span className={pred.prediction_label === 'REAL' ? 'badge-real' : pred.prediction_label === 'FAKE' ? 'badge-fake' : 'badge-inconclusive'}>
                      {pred.prediction_label}
                    </span>
                  </td>
                  <td className="fw-semibold">{(pred.confidence_score * 100).toFixed(1)}%</td>
                  <td className="small text-muted">{pred.analysis_type}</td>
                  <td className="small text-muted">
                    {pred.created_at ? new Date(pred.created_at).toLocaleString() : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
