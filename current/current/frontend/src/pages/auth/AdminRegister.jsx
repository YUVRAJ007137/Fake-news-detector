import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaUserShield, FaUser, FaEnvelope, FaLock, FaKey } from 'react-icons/fa';
import { toast } from 'react-toastify';

const AdminRegister = () => {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    username: '',
    password: '',
    confirm_password: '',
    admin_secret: ''
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.full_name || !formData.email || !formData.password || !formData.admin_secret) {
      toast.error('All fields including the Administrator Enrollment Secret are required.');
      return;
    }

    if (formData.password !== formData.confirm_password) {
      toast.error('Passwords do not match.');
      return;
    }

    if (formData.password.length < 8) {
      toast.error('Administrator password must be at least 8 characters in length.');
      return;
    }

    setLoading(true);
    try {
      await authService.adminRegister(formData);
      toast.success('Administrator account registered successfully! Please log in.');
      navigate('/admin/login');
    } catch (err) {
      toast.error(err.response?.data?.message || err.response?.data?.error || 'Admin enrollment failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <div className="container py-5 my-auto">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            <div className="card app-card p-4 p-md-5 border-0 shadow">
              <div className="text-center mb-4">
                <div className="p-3 bg-danger bg-opacity-10 text-danger rounded-circle d-inline-block mb-2">
                  <FaUserShield className="fs-2" />
                </div>
                <h3 className="fw-bold">Admin Enrollment</h3>
                <p className="text-muted small">Requires a validated server-side administrator secret code</p>
              </div>

              {/* Informative Hint */}
              <div className="alert alert-secondary py-2 px-3 small border mb-3">
                <strong>Default Bootstrap Secret:</strong> <code>AdminSecretPasscode2025!</code>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label small fw-semibold">Admin Full Name *</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaUser />
                    </span>
                    <input
                      type="text"
                      name="full_name"
                      className="form-control border-start-0"
                      placeholder="e.g. Dr. Eleanor Vance"
                      value={formData.full_name}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label small fw-semibold">Admin Email Address *</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaEnvelope />
                    </span>
                    <input
                      type="email"
                      name="email"
                      className="form-control border-start-0"
                      placeholder="admin@institution.edu"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label small fw-semibold">Password (min 8 characters) *</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaLock />
                    </span>
                    <input
                      type="password"
                      name="password"
                      className="form-control border-start-0"
                      placeholder="Secure administrator passphrase"
                      value={formData.password}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label small fw-semibold">Confirm Password *</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaLock />
                    </span>
                    <input
                      type="password"
                      name="confirm_password"
                      className="form-control border-start-0"
                      placeholder="Repeat passphrase"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label className="form-label small fw-semibold text-danger">Server Enrollment Secret *</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-danger">
                      <FaKey />
                    </span>
                    <input
                      type="password"
                      name="admin_secret"
                      className="form-control border-start-0"
                      placeholder="Enter server-side secret"
                      value={formData.admin_secret}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="btn btn-danger w-100 py-2 fw-semibold d-flex align-items-center justify-content-center gap-2"
                >
                  <FaUserShield /> {loading ? 'Enrolling...' : 'Enroll Administrator'}
                </button>
              </form>

              <div className="text-center mt-4 small text-muted">
                Already have admin credentials?{' '}
                <Link to="/admin/login" className="text-danger fw-semibold text-decoration-none">
                  Admin Sign In
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default AdminRegister;
