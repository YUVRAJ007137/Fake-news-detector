import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {
  FaTachometerAlt, FaHistory, FaNewspaper, FaRobot,
  FaFileUpload, FaBookmark, FaUser, FaSignOutAlt
} from 'react-icons/fa';

const UserLayout = () => {
  const { logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <div className="d-flex flex-grow-1">
        {/* Left Sidebar */}
        <aside className="app-sidebar p-3 d-none d-md-flex flex-column shadow-sm">
          <div className="mb-4 px-2">
            <span className="text-uppercase text-muted extra-small fw-bold">User Workspace</span>
          </div>

          <nav className="nav flex-column gap-1 flex-grow-1">
            <NavLink to="/user/dashboard" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaTachometerAlt /> Dashboard
            </NavLink>
            <NavLink to="/user/previous-news" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaNewspaper /> Previous News ML
            </NavLink>
            <NavLink to="/user/latest-news" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaRobot /> Latest News &amp; Gemini
            </NavLink>
            <NavLink to="/user/file-upload" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaFileUpload /> File Upload Detection
            </NavLink>
            <NavLink to="/user/history" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaHistory /> Prediction History
            </NavLink>
            <NavLink to="/user/saved-news" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaBookmark /> Saved News
            </NavLink>
            <NavLink to="/user/profile" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaUser /> My Profile
            </NavLink>
          </nav>

          <div className="border-top pt-3">
            <button
              onClick={handleLogout}
              className="btn btn-outline-danger btn-sm w-100 d-flex align-items-center justify-content-center gap-2"
            >
              <FaSignOutAlt /> Log Out
            </button>
          </div>
        </aside>

        {/* Main Content Workspace */}
        <main className="flex-grow-1 p-4 overflow-auto">
          <div className="container-fluid">
            <Outlet />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
};

export default UserLayout;
