import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { authService } from '../../services/authService';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaShieldAlt, FaEnvelope, FaLock, FaSignInAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';

const Login = () => {
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
      const res = await authService.login(formData);
      loginUser(res.user, res.access_token);
      toast.success('Welcome back! Login successful.');
      navigate('/user/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Invalid credentials.');
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
                <div className="p-3 bg-primary-light text-primary rounded-circle d-inline-block mb-2">
                  <FaShieldAlt className="fs-2" />
                </div>
                <h3 className="fw-bold">User Sign In</h3>
                <p className="text-muted small">Access your fake news detection workspace</p>
              </div>

              {/* Demo Credentials Alert */}
              <div className="alert alert-info py-2 px-3 small border mb-3">
                <strong>Demo Account:</strong> <code>user@fakenews.ai</code> / <code>User@12345</code>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label small fw-semibold">Email Address</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaEnvelope />
                    </span>
                    <input
                      type="email"
                      name="email"
                      className="form-control border-start-0"
                      placeholder="name@example.com"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label className="form-label small fw-semibold">Password</label>
                  <div className="input-group">
                    <span className="input-group-text bg-white border-end-0 text-muted">
                      <FaLock />
                    </span>
                    <input
                      type="password"
                      name="password"
                      className="form-control border-start-0"
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="btn btn-primary w-100 py-2 fw-semibold d-flex align-items-center justify-content-center gap-2"
                >
                  <FaSignInAlt /> {loading ? 'Signing in...' : 'Sign In'}
                </button>
              </form>

              <div className="text-center mt-4 small text-muted">
                Don't have an account?{' '}
                <Link to="/register" className="text-primary fw-semibold text-decoration-none">
                  Create one now
                </Link>
              </div>

              <div className="text-center mt-2 small text-muted">
                Administrator?{' '}
                <Link to="/admin/login" className="text-secondary text-decoration-none">
                  Admin Login
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

export default Login;
