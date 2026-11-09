import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { authService } from '../../services/authService';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaUserShield, FaEnvelope, FaLock, FaKey } from 'react-icons/fa';
import { toast } from 'react-toastify';

const AdminLogin = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      toast.error('Please enter both email and password.');
      return;
    }

    setLoading(true);
    try {
      const res = await authService.adminLogin(formData);
      loginUser(res.user, res.access_token);
      toast.success('Administrator authenticated successfully.');
      navigate('/admin/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Invalid administrator credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <div className="container py-5 my-auto">
        <div className="row justify-content-center">
          <div className="col-md-5">
            <div className="card app-card p-4 p-md-5 border-0 shadow">
              <div className="text-center mb-4">
                <div className="p-3 bg-danger bg-opacity-10 text-danger rounded-circle d-inline-block mb-2">
                  <FaUserShield className="fs-2" />
                </div>
                <h3 className="fw-bold">Administrator Portal</h3>
                <p className="text-muted small">Restricted governance, dataset &amp; model retraining console</p>
              </div>

              {/* Demo Admin Alert */}
              <div className="alert alert-warning py-2 px-3 small border mb-3">
                <strong>Default Admin:</strong> <code>admin@fakenews.ai</code> / <code>Admin@12345</code>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label small fw-semibold">Admin Email</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaEnvelope />
                    </span>
                    <input
                      type="email"
                      name="email"
                      className="form-control border-start-0"
                      placeholder="admin@domain.com"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label className="form-label small fw-semibold">Admin Password</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaLock />
                    </span>
                    <input
                      type="password"
                      name="password"
                      className="form-control border-start-0"
                      placeholder="Enter administrator password"
                      value={formData.password}
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
                  <FaKey /> {loading ? 'Authenticating...' : 'Enter Admin Console'}
                </button>
              </form>

              <div className="text-center mt-4 small text-muted">
                Authorized enrollment key?{' '}
                <Link to="/admin/register" className="text-danger fw-semibold text-decoration-none">
                  Enroll New Admin
                </Link>
              </div>

              <div className="text-center mt-2 small text-muted">
                Standard user?{' '}
                <Link to="/login" className="text-primary text-decoration-none">
                  User Login
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

export default AdminLogin;
