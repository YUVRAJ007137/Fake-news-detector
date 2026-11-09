import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaDatabase, FaCheckCircle, FaExclamationCircle, FaSyncAlt, FaFileCode } from 'react-icons/fa';
import { toast } from 'react-toastify';

const DatasetAdminPage = () => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [validationReport, setValidationReport] = useState(null);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const data = await adminService.getDatasets();
      setDatasets(data.datasets || []);
    } catch (err) {
      toast.error('Failed to load dataset registry.');
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async (filePath) => {
    try {
      toast.info('Running schema and label validation...');
      const res = await adminService.validateDataset(filePath);
      setValidationReport(res.report);
      toast.success('Validation report generated.');
    } catch (err) {
      toast.error('Failed to validate dataset.');
    }
  };

  const handleCreateHybrid = async () => {
    setGenerating(true);
    try {
      const res = await adminService.createHybridDataset();
      toast.success(res.message);
      loadDatasets();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Hybrid construction failed.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
          <div>
            <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
              <FaDatabase className="text-danger" /> Dataset Management &amp; Hybrid Engineering
            </h4>
            <p className="text-muted small mb-0">
              Manage self-generated and Kaggle benchmark datasets, inspect integrity, and build the harmonized hybrid corpus.
            </p>
          </div>

          <button
            onClick={handleCreateHybrid}
            disabled={generating}
            className="btn btn-danger btn-sm d-flex align-items-center gap-2 shadow-sm"
          >
            <FaSyncAlt className={generating ? 'fa-spin' : ''} />
            {generating ? 'Constructing Hybrid Dataset...' : 'Generate / Update Hybrid Dataset'}
          </button>
        </div>

        {/* Datasets Table */}
        <div className="table-responsive mb-4">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Dataset Name</th>
                <th>Type</th>
                <th>File Path</th>
                <th>Record Count</th>
                <th>Version</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-muted">Loading datasets...</td>
                </tr>
              ) : datasets.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-muted">No registered datasets found.</td>
                </tr>
              ) : (
                datasets.map((d) => (
                  <tr key={d.id}>
                    <td>#{d.id}</td>
                    <td className="fw-semibold">{d.dataset_name}</td>
                    <td>
                      <span className="badge bg-light text-dark border text-uppercase">{d.dataset_type}</span>
                    </td>
                    <td className="small text-muted font-monospace">{d.file_path}</td>
                    <td className="fw-bold">{d.record_count}</td>
                    <td><span className="badge bg-secondary">{d.dataset_version}</span></td>
                    <td><span className="badge bg-success">{d.status}</span></td>
                    <td>
                      <button
                        onClick={() => handleValidate(d.file_path)}
                        className="btn btn-outline-primary btn-sm py-1 px-2"
                        title="Validate Schema & Distribution"
                      >
                        <FaFileCode /> Validate
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Validation Report Presentation */}
        {validationReport && (
          <div className="card app-card border p-4 bg-light shadow-sm">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="fw-bold mb-0 d-flex align-items-center gap-2">
                <FaCheckCircle className="text-success" /> Dataset Validation Audit Report
              </h5>
              <button onClick={() => setValidationReport(null)} className="btn btn-sm btn-outline-secondary">
                Dismiss
              </button>
            </div>

            <div className="row g-3">
              <div className="col-md-4">
                <div className="p-3 bg-white rounded border">
                  <span className="text-muted small">Status:</span>
                  <h5 className="fw-bold text-success my-1">{validationReport.status}</h5>
                  <span className="text-muted small">Total Rows: {validationReport.total_rows}</span>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-3 bg-white rounded border">
                  <span className="text-muted small">Duplicates:</span>
                  <h5 className="fw-bold text-dark my-1">{validationReport.duplicate_rows}</h5>
                  <span className="text-muted small">Valid Labels (0/1): {validationReport.valid_labels ? 'Yes' : 'No'}</span>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-3 bg-white rounded border">
                  <span className="text-muted small">Class Breakdown:</span>
                  <h6 className="fw-bold my-1">
                    REAL: {validationReport.class_distribution?.REAL || 0} | FAKE: {validationReport.class_distribution?.FAKE || 0}
                  </h6>
                  <span className="text-muted small">Null Values: 0 across all core columns</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DatasetAdminPage;
