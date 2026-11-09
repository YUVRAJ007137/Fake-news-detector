import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaFolderOpen, FaFilePdf, FaFileWord, FaFileAlt, FaFileCsv } from 'react-icons/fa';
import { toast } from 'react-toastify';

const FilesAdminPage = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const data = await adminService.getFiles();
      setFiles(data.files || []);
    } catch (err) {
      toast.error('Failed to load uploaded files audit.');
    } finally {
      setLoading(false);
    }
  };

  const getFileIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'pdf': return <FaFilePdf className="text-danger" />;
      case 'docx': return <FaFileWord className="text-primary" />;
      case 'csv': return <FaFileCsv className="text-success" />;
      default: return <FaFileAlt className="text-secondary" />;
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="mb-4">
          <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <FaFolderOpen className="text-danger" /> System Uploaded Documents Audit
          </h4>
          <p className="text-muted small mb-0">
            Audit logs of all files uploaded for single-article or batch CSV news detection.
          </p>
        </div>

        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>File ID</th>
                <th>Original Filename</th>
                <th>Format</th>
                <th>Analysis Mode</th>
                <th>Articles Count</th>
                <th>Processing Status</th>
                <th>User ID</th>
                <th>Upload Date</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-muted">Loading file audit logs...</td>
                </tr>
              ) : files.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-muted">No documents uploaded yet.</td>
                </tr>
              ) : (
                files.map((f) => (
                  <tr key={f.id}>
                    <td>#{f.id}</td>
                    <td className="fw-semibold d-flex align-items-center gap-2">
                      {getFileIcon(f.file_type)} {f.original_filename}
                    </td>
                    <td>
                      <span className="badge bg-light text-dark border text-uppercase">{f.file_type}</span>
                    </td>
                    <td className="small text-muted">{f.analysis_mode}</td>
                    <td>
                      <span className="badge bg-secondary">{f.records_count} articles</span>
                    </td>
                    <td>
                      <span className={`badge ${f.processing_status === 'COMPLETED' ? 'bg-success' : 'bg-warning'}`}>
                        {f.processing_status}
                      </span>
                    </td>
                    <td>{f.user_id ? `#${f.user_id}` : 'Anonymous'}</td>
                    <td className="small text-muted">
                      {f.uploaded_at ? new Date(f.uploaded_at).toLocaleString() : '-'}
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

export default FilesAdminPage;
