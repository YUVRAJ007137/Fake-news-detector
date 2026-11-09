import React, { useState } from 'react';
import { newsService } from '../../services/newsService';
import PredictionCard from '../../components/PredictionCard';
import { FaNewspaper, FaMagic, FaEraser, FaSearch } from 'react-icons/fa';
import { toast } from 'react-toastify';

const SAMPLE_REAL = {
  title: 'Quantum Computing Milestone Reached as Commercial Cryogenic Processor Stabilizes',
  article: 'Researchers at leading computational laboratories have demonstrated quantum coherence exceeding 150 microseconds on a commercial silicon-spin processor operating below 1 Kelvin. The published benchmark confirms error-mitigation thresholds suitable for surface code quantum simulation.',
  category: 'Technology',
  source: 'Institute of Quantum Engineering'
};

const SAMPLE_FAKE = {
  title: 'Secret Subterranean City Discovered Beneath Antarctic Ice Shelf Houses Ancient Alien Technology',
  article: 'Whistleblower claims naval researchers uncovered a 50,000-year-old alien complex buried 2 miles beneath the ice sheet that powers a planetary weather control device suppressed by global elites.',
  category: 'Science',
  source: 'Conspiracy Viral Post'
};

const PreviousNewsPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    article: '',
    category: 'General',
    source: 'User Input'
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const loadSample = (sample) => {
    setFormData(sample);
    setResult(null);
  };

  const handleClear = () => {
    setFormData({
      title: '',
      article: '',
      category: 'General',
      source: 'User Input'
    });
    setResult(null);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!formData.title.trim() || !formData.article.trim()) {
      toast.error('Both News Title and News Article text are required.');
      return;
    }

    if (formData.article.trim().length < 20) {
      toast.warning('Article content is too short (minimum 20 characters).');
      return;
    }

    setLoading(true);
    try {
      const res = await newsService.predictPreviousNews(
        formData.title,
        formData.article,
        formData.category,
        formData.source
      );
      setResult(res.result);
      toast.success(res.message || 'Prediction generated successfully.');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-lg-10">
        <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
          <div className="d-flex flex-wrap justify-content-between align-items-center mb-3">
            <div>
              <h4 className="fw-bold text-dark d-flex align-items-center gap-2 mb-1">
                <FaNewspaper className="text-primary" /> Previous News Detection
              </h4>
              <p className="text-muted small mb-0">
                Linguistic pattern classification using our pre-trained Calibrated Linear SVM &amp; TF-IDF vectorizer.
              </p>
            </div>

            {/* Quick Demo Pre-fill Buttons */}
            <div className="d-flex gap-2 mt-2 mt-sm-0">
              <button
                type="button"
                onClick={() => loadSample(SAMPLE_REAL)}
                className="btn btn-outline-success btn-sm d-flex align-items-center gap-1"
              >
                <FaMagic /> Load Sample Real
              </button>
              <button
                type="button"
                onClick={() => loadSample(SAMPLE_FAKE)}
                className="btn btn-outline-danger btn-sm d-flex align-items-center gap-1"
              >
                <FaMagic /> Load Sample Fake
              </button>
            </div>
          </div>

          <form onSubmit={handleAnalyze}>
            <div className="mb-3">
              <label className="form-label small fw-semibold">News Headline / Title *</label>
              <input
                type="text"
                name="title"
                className="form-control"
                placeholder="Paste the news article title or headline..."
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <label className="form-label small fw-semibold">Category</label>
                <select
                  name="category"
                  className="form-select"
                  value={formData.category}
                  onChange={handleChange}
                >
                  <option value="General">General News</option>
                  <option value="Politics">Politics &amp; Government</option>
                  <option value="Health">Health &amp; Medicine</option>
                  <option value="Technology">Technology &amp; AI</option>
                  <option value="Science">Science &amp; Space</option>
                  <option value="Business">Business &amp; Economy</option>
                  <option value="Education">Education &amp; Society</option>
                </select>
              </div>

              <div className="col-md-6">
                <label className="form-label small fw-semibold">Source / Publisher (Optional)</label>
                <input
                  type="text"
                  name="source"
                  className="form-control"
                  placeholder="e.g. Associated Press, Blog, Social Media"
                  value={formData.source}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="form-label small fw-semibold">News Article Body *</label>
              <textarea
                name="article"
                rows="6"
                className="form-control"
                placeholder="Paste the full news article body or content to analyze..."
                value={formData.article}
                onChange={handleChange}
                required
              ></textarea>
              <div className="form-text small text-end">
                Character count: {formData.article.length}
              </div>
            </div>

            <div className="d-flex gap-2">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary px-4 py-2 fw-semibold d-flex align-items-center gap-2"
              >
                <FaSearch /> {loading ? 'Analyzing Linguistic Patterns...' : 'Analyze News Authenticity'}
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="btn btn-outline-secondary px-3 py-2 d-flex align-items-center gap-1"
              >
                <FaEraser /> Clear
              </button>
            </div>
          </form>

          {/* Result Presentation */}
          {result && (
            <PredictionCard
              result={result}
              newsId={result.news_id}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default PreviousNewsPage;
