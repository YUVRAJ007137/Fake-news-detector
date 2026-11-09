import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaListAlt, FaShieldAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';

const AdminLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await adminService.getAdminLogs();
      setLogs(data.logs || []);
    } catch (err) {
      toast.error('Failed to load administrative security logs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="mb-4">
          <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <FaListAlt className="text-danger" /> System Administrator Security Audit Logs
          </h4>
          <p className="text-muted small mb-0">
            Immutable log of sensitive administrative events, logins, model promotions, and user activations.
          </p>
        </div>

        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>Log ID</th>
                <th>Administrator</th>
                <th>Action Performed</th>
                <th>Target Resource</th>
                <th>Target ID</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">Loading audit records...</td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">No administrative logs recorded yet.</td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id}>
                    <td>#{log.id}</td>
                    <td className="fw-semibold">{log.admin_name} (#{log.admin_id})</td>
                    <td>
                      <span className="badge bg-light text-dark border font-monospace">{log.action}</span>
                    </td>
                    <td>
                      <span className="badge bg-secondary text-uppercase">{log.target_type}</span>
                    </td>
                    <td>{log.target_id ? `#${log.target_id}` : '-'}</td>
                    <td className="small text-muted">
                      {log.created_at ? new Date(log.created_at).toLocaleString() : '-'}
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

export default AdminLogsPage;
