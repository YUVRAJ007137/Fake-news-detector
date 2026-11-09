import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Public Pages
import LandingPage from './pages/LandingPage';
import AboutPage from './pages/AboutPage';
import HowItWorksPage from './pages/HowItWorksPage';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import AdminLogin from './pages/auth/AdminLogin';
import AdminRegister from './pages/auth/AdminRegister';

// Layouts
import UserLayout from './layouts/UserLayout';
import AdminLayout from './layouts/AdminLayout';

// User Pages
import UserDashboard from './pages/user/UserDashboard';
import PreviousNewsPage from './pages/user/PreviousNewsPage';
import LatestNewsPage from './pages/user/LatestNewsPage';
import FileUploadPage from './pages/user/FileUploadPage';
import PredictionHistoryPage from './pages/user/PredictionHistoryPage';
import SavedNewsPage from './pages/user/SavedNewsPage';
import ProfilePage from './pages/user/ProfilePage';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagementPage from './pages/admin/UserManagementPage';
import PredictionsAdminPage from './pages/admin/PredictionsAdminPage';
import FilesAdminPage from './pages/admin/FilesAdminPage';
import DatasetAdminPage from './pages/admin/DatasetAdminPage';
import ModelTrainingPage from './pages/admin/ModelTrainingPage';
import GeminiRecordsPage from './pages/admin/GeminiRecordsPage';
import AdminLogsPage from './pages/admin/AdminLogsPage';

// Route Guards
const UserRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="text-center p-5">Loading security context...</div>;
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  if (loading) return <div className="text-center p-5">Verifying administrator credentials...</div>;
  return isAuthenticated && isAdmin ? children : <Navigate to="/admin/login" replace />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/how-it-works" element={<HowItWorksPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/register" element={<AdminRegister />} />

          {/* User Workspace (Protected) */}
          <Route
            path="/user"
            element={
              <UserRoute>
                <UserLayout />
              </UserRoute>
            }
          >
            <Route index element={<Navigate to="/user/dashboard" replace />} />
            <Route path="dashboard" element={<UserDashboard />} />
            <Route path="previous-news" element={<PreviousNewsPage />} />
            <Route path="latest-news" element={<LatestNewsPage />} />
            <Route path="file-upload" element={<FileUploadPage />} />
            <Route path="history" element={<PredictionHistoryPage />} />
            <Route path="saved-news" element={<SavedNewsPage />} />
            <Route path="profile" element={<ProfilePage />} />
          </Route>

          {/* Administrator Workspace (Protected) */}
          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminLayout />
              </AdminRoute>
            }
          >
            <Route index element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="dashboard" element={<AdminDashboard />} />
            <Route path="users" element={<UserManagementPage />} />
            <Route path="predictions" element={<PredictionsAdminPage />} />
            <Route path="files" element={<FilesAdminPage />} />
            <Route path="datasets" element={<DatasetAdminPage />} />
            <Route path="models" element={<ModelTrainingPage />} />
            <Route path="gemini-records" element={<GeminiRecordsPage />} />
            <Route path="logs" element={<AdminLogsPage />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>

      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </AuthProvider>
  );
}

export default App;
