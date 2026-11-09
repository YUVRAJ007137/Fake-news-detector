import api from './api';

export const adminService = {
  // Dashboard & KPIs
  async getDashboardKPIs() {
    const res = await api.get('/admin/dashboard');
    return res.data;
  },

  // Users
  async getUsers(role = '', query = '') {
    const params = {};
    if (role) params.role = role;
    if (query) params.query = query;
    const res = await api.get('/admin/users', { params });
    return res.data;
  },

  async toggleUserStatus(userId, isActive) {
    const res = await api.patch(`/admin/users/${userId}/status`, { is_active: isActive });
    return res.data;
  },

  // Predictions
  async getPredictions(label = '') {
    const params = {};
    if (label) params.label = label;
    const res = await api.get('/admin/predictions', { params });
    return res.data;
  },

  // Uploaded Files
  async getFiles() {
    const res = await api.get('/admin/files');
    return res.data;
  },

  // Datasets
  async getDatasets() {
    const res = await api.get('/admin/datasets');
    return res.data;
  },

  async validateDataset(filePath) {
    const res = await api.post('/admin/datasets/validate', { file_path: filePath });
    return res.data;
  },

  async createHybridDataset() {
    const res = await api.post('/admin/datasets/create-hybrid');
    return res.data;
  },

  // Models & Retraining
  async getModels() {
    const res = await api.get('/admin/models');
    return res.data;
  },

  async getModelMetrics() {
    const res = await api.get('/admin/models/metrics');
    return res.data;
  },

  async triggerRetraining(datasetVersion = 'v1.0.0') {
    const res = await api.post('/admin/models/train', { dataset_version: datasetVersion });
    return res.data;
  },

  async getTrainingLogs() {
    const res = await api.get('/admin/models/training-logs');
    return res.data;
  },

  // Gemini Audit Records
  async getGeminiRecords() {
    const res = await api.get('/admin/gemini-records');
    return res.data;
  },

  // System Logs
  async getAdminLogs() {
    const res = await api.get('/admin/logs');
    return res.data;
  }
};
