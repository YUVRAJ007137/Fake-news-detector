import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {
  FaTachometerAlt, FaUsers, FaHistory, FaDatabase,
  FaCogs, FaRobot, FaListAlt, FaFolderOpen, FaSignOutAlt
} from 'react-icons/fa';

const AdminLayout = () => {
  const { logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/admin/login');
  };

  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <div className="d-flex flex-grow-1">
        {/* Left Admin Sidebar */}
        <aside className="app-sidebar p-3 d-none d-md-flex flex-column shadow-sm bg-white">
          <div className="mb-4 px-2">
            <span className="badge bg-danger text-uppercase px-2 py-1">Administrator Portal</span>
          </div>

          <nav className="nav flex-column gap-1 flex-grow-1">
            <NavLink to="/admin/dashboard" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaTachometerAlt /> Overview KPIs
            </NavLink>
            <NavLink to="/admin/users" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaUsers /> User Governance
            </NavLink>
            <NavLink to="/admin/predictions" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaHistory /> All Predictions
            </NavLink>
            <NavLink to="/admin/files" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaFolderOpen /> Uploaded Files
            </NavLink>
            <NavLink to="/admin/datasets" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaDatabase /> Dataset Operations
            </NavLink>
            <NavLink to="/admin/models" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaCogs /> Retraining &amp; Models
            </NavLink>
            <NavLink to="/admin/gemini-records" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaRobot /> Gemini Audit Trail
            </NavLink>
            <NavLink to="/admin/logs" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <FaListAlt /> Security Action Logs
            </NavLink>
          </nav>

          <div className="border-top pt-3">
            <button
              onClick={handleLogout}
              className="btn btn-outline-danger btn-sm w-100 d-flex align-items-center justify-content-center gap-2"
            >
              <FaSignOutAlt /> Admin Exit
            </button>
          </div>
        </aside>

        {/* Main Admin Workspace */}
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

export default AdminLayout;
