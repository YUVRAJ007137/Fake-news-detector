import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaShieldAlt, FaSignOutAlt, FaUserCircle, FaTachometerAlt } from 'react-icons/fa';

const Navbar = () => {
  const { user, isAuthenticated, isAdmin, logoutUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  const isAuthRoute = location.pathname.includes('/login') || location.pathname.includes('/register');

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top shadow-sm py-2">
      <div className="container-fluid px-4">
        <Link className="navbar-brand navbar-brand-custom" to="/">
          <FaShieldAlt className="text-primary fs-3" />
          <span>VeriNews</span> <small className="text-muted fw-normal fs-6">| AI News Guard</small>
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarMainContent"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarMainContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
            <li className="nav-item">
              <Link className="nav-link" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/about">About Project</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/how-it-works">How It Works</Link>
            </li>
          </ul>

          <div className="d-flex align-items-center gap-2">
            {isAuthenticated ? (
              <>
                <Link
                  to={isAdmin ? '/admin/dashboard' : '/user/dashboard'}
                  className="btn btn-outline-primary btn-sm d-flex align-items-center gap-1"
                >
                  <FaTachometerAlt /> {isAdmin ? 'Admin Portal' : 'User Dashboard'}
                </Link>
                <div className="d-flex align-items-center gap-2 border-start ps-3 ms-2">
                  <FaUserCircle className="text-secondary fs-4" />
                  <div className="d-none d-md-block text-start lh-1">
                    <span className="fw-semibold small d-block">{user?.full_name}</span>
                    <span className="badge bg-light text-dark border extra-small mt-1">{user?.role?.toUpperCase()}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="btn btn-sm btn-outline-danger ms-2 d-flex align-items-center gap-1"
                    title="Log Out"
                  >
                    <FaSignOutAlt /> <span className="d-none d-md-inline">Logout</span>
                  </button>
                </div>
              </>
            ) : (
              !isAuthRoute && (
                <div className="d-flex gap-2">
                  <Link to="/login" className="btn btn-outline-primary btn-sm px-3">
                    User Login
                  </Link>
                  <Link to="/register" className="btn btn-primary btn-sm px-3">
                    Register
                  </Link>
                  <Link to="/admin/login" className="btn btn-outline-secondary btn-sm px-2" title="Admin Portal">
                    Admin
                  </Link>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
