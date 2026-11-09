import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { FaUsers, FaSearch, FaUserCheck, FaUserSlash } from 'react-icons/fa';
import { toast } from 'react-toastify';

const UserManagementPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState('');
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetchUsers();
  }, [roleFilter]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await adminService.getUsers(roleFilter, query);
      setUsers(data.users || []);
    } catch (err) {
      toast.error('Failed to load user records.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (user) => {
    try {
      const res = await adminService.toggleUserStatus(user.id, !user.is_active);
      toast.success(res.message);
      setUsers(users.map((u) => (u.id === user.id ? { ...u, is_active: !u.is_active } : u)));
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to update user status.');
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchUsers();
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
          <div>
            <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
              <FaUsers className="text-danger" /> User Account Governance
            </h4>
            <p className="text-muted small mb-0">
              Audit registered citizen accounts, inspect roles, and manage authorization status.
            </p>
          </div>

          <form onSubmit={handleSearch} className="d-flex gap-2">
            <input
              type="text"
              className="form-control form-control-sm"
              placeholder="Search by name or email..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit" className="btn btn-primary btn-sm d-flex align-items-center gap-1">
              <FaSearch /> Search
            </button>
          </form>
        </div>

        {/* Role Tabs */}
        <div className="d-flex gap-2 mb-4">
          <button
            onClick={() => setRoleFilter('')}
            className={`btn btn-sm ${roleFilter === '' ? 'btn-primary' : 'btn-outline-secondary'}`}
          >
            All Accounts
          </button>
          <button
            onClick={() => setRoleFilter('user')}
            className={`btn btn-sm ${roleFilter === 'user' ? 'btn-primary' : 'btn-outline-secondary'}`}
          >
            Users Only
          </button>
          <button
            onClick={() => setRoleFilter('admin')}
            className={`btn btn-sm ${roleFilter === 'admin' ? 'btn-primary' : 'btn-outline-secondary'}`}
          >
            Administrators
          </button>
        </div>

        {/* Users Table */}
        <div className="table-responsive">
          <table className="table table-custom table-hover">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Full Name</th>
                <th>Email Address</th>
                <th>Role</th>
                <th>Account Status</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">Loading user accounts...</td>
                </tr>
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">No users found.</td>
                </tr>
              ) : (
                users.map((u) => (
                  <tr key={u.id}>
                    <td>#{u.id}</td>
                    <td className="fw-semibold">{u.full_name}</td>
                    <td>{u.email}</td>
                    <td>
                      <span className={`badge ${u.role === 'admin' ? 'bg-danger' : 'bg-primary'}`}>
                        {u.role.toUpperCase()}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${u.is_active ? 'bg-success' : 'bg-secondary'}`}>
                        {u.is_active ? 'Active' : 'Deactivated'}
                      </span>
                    </td>
                    <td className="small text-muted">
                      {u.created_at ? new Date(u.created_at).toLocaleDateString() : '-'}
                    </td>
                    <td>
                      <button
                        onClick={() => handleToggleStatus(u)}
                        className={`btn btn-sm ${u.is_active ? 'btn-outline-danger' : 'btn-outline-success'} py-1 px-2`}
                        title={u.is_active ? 'Deactivate Account' : 'Activate Account'}
                      >
                        {u.is_active ? <><FaUserSlash /> Deactivate</> : <><FaUserCheck /> Activate</>}
                      </button>
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

export default UserManagementPage;
