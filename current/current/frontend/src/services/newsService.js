import api from './api';

export const newsService = {
  // Previous News Detection using trained ML model
  async predictPreviousNews(title, article, category = 'General', source = 'User Input') {
    const res = await api.post('/news/predict', { title, article, category, source });
    return res.data;
  },

  // Latest News Analysis using ML + Gemini API
  async analyzeLatestNews(title, article, category = 'General', source = 'Latest News') {
    const res = await api.post('/news/latest-analysis', { title, article, category, source });
    return res.data;
  },

  // Prediction History
  async getHistory(label = '', query = '') {
    const params = {};
    if (label) params.label = label;
    if (query) params.query = query;
    const res = await api.get('/news/history', { params });
    return res.data;
  },

  async getHistoryById(id) {
    const res = await api.get(`/news/history/${id}`);
    return res.data;
  },

  // Saved News
  async saveNews(newsId) {
    const res = await api.post('/news/save', { news_id: newsId });
    return res.data;
  },

  async removeSavedNews(newsId) {
    const res = await api.delete(`/news/save/${newsId}`);
    return res.data;
  },

  async getSavedNews() {
    const res = await api.get('/news/saved');
    return res.data;
  }
};
