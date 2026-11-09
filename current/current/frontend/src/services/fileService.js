import api from './api';

export const fileService = {
  // Upload and analyze file (PDF, DOCX, TXT, CSV)
  async uploadFile(file, analysisMode = 'ml_previous') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('analysis_mode', analysisMode);

    const res = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  async getUploadHistory() {
    const res = await api.get('/files/history');
    return res.data;
  }
};
