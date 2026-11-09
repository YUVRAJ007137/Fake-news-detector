import React, { useState } from 'react';
import { fileService } from '../../services/fileService';
import PredictionCard from '../../components/PredictionCard';
import {
  FaFileUpload, FaFilePdf, FaFileWord, FaFileAlt,
  FaFileCsv, FaCheckCircle, FaExclamationTriangle, FaDownload
} from 'react-icons/fa';
import { toast } from 'react-toastify';

const FileUploadPage = () => {
  const [file, setFile] = useState(null);
  const [analysisMode, setAnalysisMode] = useState('ml_previous');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResponse(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      toast.error('Please select a file to upload.');
      return;
    }

    setLoading(true);
    try {
      const res = await fileService.uploadFile(file, analysisMode);
      setResponse(res);
      toast.success(res.message || 'File processed successfully.');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Document processing failed.');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    if (!response || !response.result) return;
    const blob = new Blob([JSON.stringify(response.result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `detection_report_${response.filename || 'upload'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="row justify-content-center">
      <div className="col-lg-10">
        <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
          <div className="mb-4">
            <h4 className="fw-bold text-dark d-flex align-items-center gap-2 mb-1">
              <FaFileUpload className="text-primary" /> Multi-Format File Upload Detection
            </h4>
            <p className="text-muted small mb-0">
              Upload news files in PDF, Word (DOCX), plain text (TXT), or tabular CSV format for automatic extraction and classification.
            </p>
          </div>

          <form onSubmit={handleUpload}>
            <div className="row g-3 mb-4">
              <div className="col-md-7">
                <label className="form-label small fw-semibold">Select Document File</label>
                <input
                  type="file"
                  className="form-control"
                  accept=".pdf,.docx,.txt,.csv"
                  onChange={handleFileChange}
                  required
                />
                <div className="form-text small">
                  Supported formats: <strong>.pdf</strong>, <strong>.docx</strong>, <strong>.txt</strong>, <strong>.csv</strong> (Max 10MB)
                </div>
              </div>

              <div className="col-md-5">
                <label className="form-label small fw-semibold">Analysis Mode</label>
                <select
                  className="form-select"
                  value={analysisMode}
                  onChange={(e) => setAnalysisMode(e.target.value)}
                >
                  <option value="ml_previous">Previous News (Local ML Model)</option>
                  <option value="gemini_latest">Latest News (ML + Gemini Dual-Engine)</option>
                </select>
                <div className="form-text small">
                  Select whether to use classical ML only or include LLM claim verification.
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !file}
              className="btn btn-primary px-4 py-2 fw-semibold d-flex align-items-center gap-2"
            >
              <FaFileUpload /> {loading ? 'Extracting & Analyzing Content...' : 'Upload & Process Document'}
            </button>
          </form>

          {/* Results Presentation */}
          {response && response.result && (
            <div className="mt-4 pt-3 border-top">
              {/* Batch CSV Result */}
              {response.result.is_batch ? (
                <div>
                  <div className="d-flex flex-wrap justify-content-between align-items-center mb-3">
                    <h5 className="fw-bold mb-0">Batch CSV Analysis Summary</h5>
                    <button
                      onClick={downloadReport}
                      className="btn btn-outline-primary btn-sm d-flex align-items-center gap-1"
                    >
                      <FaDownload /> Download Report JSON
                    </button>
                  </div>

                  {/* Summary Metric Cards */}
                  <div className="row g-3 mb-4">
                    <div className="col-md-3">
                      <div className="card p-3 border bg-light text-center">
                        <span className="text-muted small">Total Processed</span>
                        <h4 className="fw-bold my-1">{response.result.summary.total}</h4>
                      </div>
                    </div>
                    <div className="col-md-3">
                      <div className="card p-3 border bg-light text-center">
                        <span className="text-success small fw-semibold">Verified Real</span>
                        <h4 className="fw-bold my-1 text-success">{response.result.summary.real}</h4>
                      </div>
                    </div>
                    <div className="col-md-3">
                      <div className="card p-3 border bg-light text-center">
                        <span className="text-danger small fw-semibold">Flagged Fake</span>
                        <h4 className="fw-bold my-1 text-danger">{response.result.summary.fake}</h4>
                      </div>
                    </div>
                    <div className="col-md-3">
                      <div className="card p-3 border bg-light text-center">
                        <span className="text-warning small fw-semibold">Inconclusive</span>
                        <h4 className="fw-bold my-1 text-warning">{response.result.summary.inconclusive}</h4>
                      </div>
                    </div>
                  </div>

                  {/* Batch Table */}
                  <div className="table-responsive">
                    <table className="table table-custom table-hover">
                      <thead>
                        <tr>
                          <th>#</th>
                          <th>Headline / Title</th>
                          <th>Article Preview</th>
                          <th>Verdict</th>
                          <th>Confidence</th>
                        </tr>
                      </thead>
                      <tbody>
                        {response.result.records.map((rec) => {
                          const isR = rec.overall_decision === 'REAL';
                          const isF = rec.overall_decision === 'FAKE';
                          return (
                            <tr key={rec.row_index}>
                              <td>{rec.row_index}</td>
                              <td className="fw-semibold text-truncate" style={{ maxWidth: '240px' }}>
                                {rec.title}
                              </td>
                              <td className="small text-muted text-truncate" style={{ maxWidth: '300px' }}>
                                {rec.article_preview}
                              </td>
                              <td>
                                <span className={isR ? 'badge-real' : isF ? 'badge-fake' : 'badge-inconclusive'}>
                                  {rec.overall_decision}
                                </span>
                              </td>
                              <td>{(rec.confidence_score * 100).toFixed(1)}%</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                /* Single Document (PDF, DOCX, TXT) */
                <div>
                  <div className="alert alert-info border py-2 px-3 mb-3 small d-flex justify-content-between align-items-center">
                    <span>
                      Extracted Text from <strong>{response.filename}</strong> ({response.file_type.toUpperCase()})
                    </span>
                    <button onClick={downloadReport} className="btn btn-sm btn-link p-0 text-decoration-none">
                      Download JSON
                    </button>
                  </div>

                  <PredictionCard
                    result={response.result}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUploadPage;
