import React, { useState, useEffect } from 'react';
import { newsService } from '../../services/newsService';
import { FaBookmark, FaTrashAlt, FaNewspaper, FaExternalLinkAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';

const SavedNewsPage = () => {
  const [savedArticles, setSavedArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSavedNews();
  }, []);

  const loadSavedNews = async () => {
    try {
      const data = await newsService.getSavedNews();
      setSavedArticles(data.saved_news || []);
    } catch (err) {
      toast.error('Failed to load saved bookmarks.');
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (newsId) => {
    try {
      await newsService.removeSavedNews(newsId);
      setSavedArticles(savedArticles.filter((item) => item.news_id !== newsId));
      toast.info('Bookmark removed.');
    } catch (err) {
      toast.error('Failed to remove bookmark.');
    }
  };

  return (
    <div>
      <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
        <div className="mb-4">
          <h4 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <FaBookmark className="text-primary" /> Saved News Articles
          </h4>
          <p className="text-muted small mb-0">
            Bookmarked news articles saved for future research and verification review.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-5 text-muted">Loading saved bookmarks...</div>
        ) : savedArticles.length === 0 ? (
          <div className="text-center py-5 text-muted">
            <FaBookmark className="fs-1 text-secondary mb-3 opacity-50" />
            <h5>No saved articles yet</h5>
            <p className="small">You can bookmark news items while running predictions.</p>
          </div>
        ) : (
          <div className="row g-3">
            {savedArticles.map((item) => (
              <div key={item.id} className="col-md-6">
                <div className="card h-100 p-4 border bg-light shadow-sm">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <span className="badge bg-primary text-uppercase">{item.category || 'General'}</span>
                    <button
                      onClick={() => handleRemove(item.news_id)}
                      className="btn btn-outline-danger btn-sm p-1 border-0"
                      title="Remove Bookmark"
                    >
                      <FaTrashAlt />
                    </button>
                  </div>
                  <h6 className="fw-bold text-dark mb-2">{item.title}</h6>
                  <p className="small text-muted mb-3 text-truncate" style={{ maxHeight: '60px' }}>
                    {item.article}
                  </p>
                  <div className="mt-auto d-flex justify-content-between align-items-center small text-muted border-top pt-2">
                    <span>Source: {item.source || 'User Input'}</span>
                    <span>Saved: {new Date(item.saved_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedNewsPage;
