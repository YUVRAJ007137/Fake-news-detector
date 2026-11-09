import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { FaUserCircle, FaEnvelope, FaShieldAlt, FaCalendarAlt } from 'react-icons/fa';

const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <div className="row justify-content-center">
      <div className="col-md-7">
        <div className="card app-card border-0 shadow-sm p-4 p-md-5 bg-white">
          <div className="text-center mb-4">
            <FaUserCircle className="text-primary display-3 mb-2" />
            <h3 className="fw-bold mb-1">{user?.full_name}</h3>
            <span className="badge bg-primary px-3 py-1 text-uppercase">{user?.role}</span>
          </div>

          <div className="list-group list-group-flush mb-4">
            <div className="list-group-item d-flex justify-content-between align-items-center px-0 py-3">
              <span className="text-muted small d-flex align-items-center gap-2">
                <FaEnvelope /> Email Address
              </span>
              <strong className="text-dark">{user?.email}</strong>
            </div>

            <div className="list-group-item d-flex justify-content-between align-items-center px-0 py-3">
              <span className="text-muted small d-flex align-items-center gap-2">
                <FaShieldAlt /> Account Status
              </span>
              <span className="badge bg-success">Active &bull; Verified</span>
            </div>

            <div className="list-group-item d-flex justify-content-between align-items-center px-0 py-3">
              <span className="text-muted small d-flex align-items-center gap-2">
                <FaCalendarAlt /> User Role
              </span>
              <strong className="text-dark">{user?.role?.toUpperCase()}</strong>
            </div>
          </div>

          <div className="alert alert-light border small text-muted">
            <strong>Security Notice:</strong> All prediction queries and document uploads are bound to your user ID and recorded in our MySQL relational audit tables.
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
